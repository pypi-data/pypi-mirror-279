from __future__ import annotations

import json
import logging
import os
import pickle
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final, List
from uuid import uuid4
from zipfile import ZipFile

import click
import jmespath
import pandas as pd
import requests
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from hurry.filesize import size
from requests import JSONDecodeError, Session

from kaas_cli.types import KaasCliException

if TYPE_CHECKING:
    from .types import File_Data, Metadata

from .constants import (
    CONFIG_LOG_PATH,
    CONFIG_SESSION_PATH,
    DEVICE_LOGIN_URL,
    FILES_LIST_URL,
    FILES_URL,
    GRAPHQL_URL,
    UPLOAD_FAILURE_MESSAGE,
    UPLOAD_SUCCESS_MESSAGE,
    USER_URL,
    VAULTS_KEY_URL,
    VAULTS_ROOT_URL,
)


@dataclass(frozen=True)
class DeviceAuth:
    device_code: str
    expires_in: int
    interval: int
    user_code: str
    verification_uri: str


@dataclass(frozen=True)
class Confirmation:
    success: bool


class CustomSession(Session):
    def get(self, *args: Any, **kwargs: Any) -> Any:
        response = super().get(*args, **kwargs)
        try:
            json_response = response.json()
            if 'error' in json_response:
                raise ValueError(json_response['error'], json_response.get('message', 'No message provided'))
            return json_response
        except JSONDecodeError as e:
            logging.error(f"GET request JSON decode failed: {e}")
            raise e
        except ValueError as e:
            logging.error(f"GET request failed: {e}")
            raise e

    def post(self, *args: Any, **kwargs: Any) -> Any:
        response = super().post(*args, **kwargs)
        try:
            json_response = response.json()
            if 'error' in json_response:
                raise ValueError(json_response['error'], json_response.get('message', 'No message provided'))
            return json_response
        except JSONDecodeError as e:
            logging.error(f"POST request JSON decode failed: {e}")
            raise e
        except ValueError as e:
            logging.error(f"POST request failed: {e}")
            click.echo(f"POST request failed: {e}")
            raise e


class AuthenticatedSession(CustomSession):
    def __init__(self, access_token: str) -> None:
        super().__init__()
        self.access_token = access_token
        self.headers.update({'Authorization': f'Bearer {self.access_token}'})


class KaasClient:
    _client: Client
    _session: CustomSession
    _url: str
    _token: str | None
    _vault: str | None
    _org: str | None

    def __init__(
        self,
        url: str,
        *,
        token: str | None = None,
        vault: str | None = None,
        org: str | None = None,
    ) -> None:
        self._url = url
        self._token = token
        self._vault = vault
        self._org = org

        self._configure_logging()
        self._setup_client()
        self._session = CustomSession()
        if token:
            self._session = AuthenticatedSession(token)
        else:
            self._load_session_if_exists()

    def _setup_client(self) -> None:
        """Setup the GraphQL client."""
        transport = RequestsHTTPTransport(
            url=f'{self._url}{GRAPHQL_URL}',
            verify=True,
        )
        self._client = Client(transport=transport, fetch_schema_from_transport=True)

    def _configure_logging(self) -> None:
        """Configure logging for the application."""
        if not CONFIG_LOG_PATH.exists():
            CONFIG_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            CONFIG_LOG_PATH.touch()
        logging.basicConfig(
            filename=CONFIG_LOG_PATH,
            filemode='a',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.DEBUG,
        )

    def _load_session_if_exists(self) -> None:
        """Load session if the session file exists."""
        if CONFIG_SESSION_PATH.exists():
            self._load_session()

    def hello(self, name: str | None = None) -> str:
        response = self._client.execute(QUERY_HELLO, variable_values={'name': name} if name is not None else {})
        return response['hello']

    def _save_session(self, file_path: Path = CONFIG_SESSION_PATH) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('wb') as file:
            pickle.dump(self._session, file)

    def _load_session(self, file_path: Path = CONFIG_SESSION_PATH) -> None:
        with file_path.open('rb') as file:
            self._session = pickle.load(file)

    def _remove_session(self, file_path: Path = CONFIG_SESSION_PATH) -> bool:
        file_path.unlink()
        return True

    def _list_local_files(self, directory: str) -> list[Path]:
        return [path for path in Path(directory).glob('**/*') if path.is_file()]

    def list_local_proofs(self, directory: str) -> list[dict[str, Any]]:
        list_local_files = [
            {
                'name': self._read_proof(path / 'proof.json').get('id'),
                'size': size(sum(f.stat().st_size for f in path.glob('**/*') if f.is_file())),
                'last_update_date': self._read_proof(path / 'proof.json').get('last_update_date'),
            }
            for path in Path(directory).glob('**/*')
            if path.is_dir() and len(path.name.split(':')) == 2
        ]
        return list_local_files

    def _read_proof(self, proof_path: Path) -> dict[str, Any]:
        if not proof_path.exists():
            return {'id': None, 'last_update_date': None}

        with proof_path.open() as file:
            data = json.load(file)
            return {
                'id': data.get('id'),
                'last_update_date': datetime.fromtimestamp(os.path.getmtime(proof_path)).isoformat(),
            }

    def list_remote(self) -> Any:
        try:
            json_data = self._session.get(url=f'{self._url}{USER_URL}')
        except Exception:
            raise KaasCliException("List remote proofs failed") from None
        return json_data

    def _get_default_vault(self) -> str | None:
        try:
            json_data = self._session.get(url=f'{self._url}{USER_URL}')
        except Exception:
            raise KaasCliException("Get default vault failed") from None
        vault_hash = jmespath.search('vaults[0].id', json_data)
        return vault_hash

    def _get_upload_urls(self, metadata: dict[str, Any], vault: str, org: str, tag: str | None) -> dict[str, Any]:
        data = self._session.post(
            url=f'{self._url}{FILES_URL.format(org, vault)}',
            data=json.dumps(
                {
                    'files': metadata,
                    'tag': tag,
                }
            ),
            headers={
                'Content-Type': 'application/json',
            },
        )
        return data["data"]

    def _upload_presigned_url(self, files: dict[str, Any], directory: str = '') -> dict[str, Any]:
        upload_results: Any = {}
        for file_path_str, url in files.items():
            file_path = Path(directory) / file_path_str
            with file_path.open('rb') as file:
                response = requests.put(url, data=file)

                # Check if the upload was successful
                if response.status_code in [200, 201]:  # Success status codes can vary, e.g., 200 OK or 201 Created
                    print(f"Successfully uploaded: {file_path}")
                    upload_results[file_path_str] = {'success': True, 'status_code': response.status_code}
                else:
                    print(f"Failed to upload {file_path.name} to {url}. Status code: {response.status_code}")
                    upload_results[file_path_str] = {
                        'success': False,
                        'status_code': response.status_code,
                        'error_message': response.text,
                    }

        return upload_results

    def archive_files(
        self, file_list: List[Path], archive_name: str, archive_format: str = 'zip', root_dir: Path | None = None
    ) -> str:
        """
        Archives a list of files into a single archive file while preserving the directory structure.

        Args: file_list (List[Path]): List of file paths to include in the archive. archive_name (str): The name of
        the output archive file without extension. archive_format (str): Format of the archive ('zip', 'tar',
        etc.). Default is 'zip'. root_dir (Path): The root directory to use for preserving the relative paths. If
        None, the common parent of all files will be used.

        Returns:
        str: The path to the created archive file.
        """
        if root_dir is None:
            # Find the common parent directory of all files
            common_paths: set[Path] = set(Path(file_list[0]).parents)
            for file_path in file_list[1:]:
                common_paths = set(common_paths) & set(Path(file_path).parents)
            root_dir = min(common_paths, key=lambda p: len(p.parts))

        # Ensure the archive name does not include an extension
        archive_path = Path(archive_name).with_suffix('')

        # Create a temporary directory to hold the files to be archived
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            for file_path in file_list:
                if file_path.is_file():
                    # Calculate relative path to the root_dir
                    relative_path = file_path.relative_to(root_dir)
                    # Create any necessary directories
                    (temp_dir_path / relative_path).parent.mkdir(parents=True, exist_ok=True)
                    # Copy file to the new location preserving the folder structure
                    shutil.copy(file_path, temp_dir_path / relative_path)

            # Create the archive from the temporary directory
            archive_final_path = shutil.make_archive(str(archive_path), archive_format, root_dir=temp_dir_path)

        # Move the archive to the desired directory and return the new path
        final_archive_path = Path(archive_final_path).with_suffix(f'.{archive_format}')
        shutil.move(archive_final_path, final_archive_path)

        return str(Path(archive_final_path))

    def get_archive_metadata(self, archive_path: str) -> dict[str, Any]:
        """
        Extracts metadata from an archive file.

        Args:
        archive_path (str): Path to the archive file.

        Returns:
        dict[str, Any]: Metadata extracted from the archive file.
        """
        # Initialize an empty dictionary for metadata
        metadata = {}

        # Create a Path object from the archive_path
        archive_file = Path(archive_path)

        # Check if the archive file exists
        if not archive_file.exists():
            raise FileNotFoundError(f"The archive file {archive_path} does not exist.")
        #             metadata[file_uuid] = {'filename': file_name_str, 'updated_at': updated_at}
        # Try to extract metadata from the archive file
        try:
            metadata[archive_file.name] = {
                'filename': archive_file.name,
                'updated_at': datetime.fromtimestamp(archive_file.stat().st_mtime).isoformat(),
            }
        except Exception as e:
            # Handle any exception that might occur during metadata extraction
            raise e

        return metadata

    def get_version_from_digest(self, file_list: Any) -> str:
        """
        Reads a JSON file named 'digest' from the provided file list, extracts hash values from specified fields,
        and returns them as a string.

        Args:
        file_list (list[Path]): List of file paths.

        Returns:
        str: A string containing the hash values from the 'digest' file.
        """
        # Find the 'digest' file in the file list
        digest_file = next((file for file in file_list if file.name == 'digest'), None)
        if digest_file is None:
            raise FileNotFoundError("No 'digest' file found in the provided file list.")

        # Read the 'digest' JSON file
        with open(digest_file, 'r') as file:
            data = json.load(file)

        # Extract the hash values from specified fields
        kompilation_hash = data.get('kompilation', 'Not found')
        foundry_hash = data.get('foundry', 'Not found')

        # Return the hash values as a string
        return f"{kompilation_hash}{foundry_hash}"

    def upload_files_s3(self, directory: str, tag: str | None = None) -> str | None:
        file_list = self._list_local_files(directory)
        if not file_list or len(file_list) == 0:
            raise ValueError(f'No files to upload in dir: {directory}')

        archive_name = self.get_version_from_digest(file_list)
        archive_path = self.archive_files(file_list, archive_name, archive_format='zip', root_dir=Path(directory))
        metadata = self.get_archive_metadata(archive_path)

        if self._vault is None or self._org is None:
            return UPLOAD_FAILURE_MESSAGE
        urls = self._get_upload_urls(metadata=metadata, vault=self._vault, tag=tag, org=self._org)

        filenames: list[str] = []
        for value in metadata.values():
            filenames.append(value['filename'])

        try:
            click.echo(f"Uploading {metadata} to S3...")
            self._upload_presigned_url(urls)
            click.echo(UPLOAD_SUCCESS_MESSAGE)
        except Exception as e:
            raise KaasCliException(f"Failed to upload {archive_path} to S3: {e}") from None
        # remove the archive file after uploading
        os.remove(archive_path)

        return None

    def download_version_or_tag(
        self, org_name: str, vault_name: str, version_or_tag: str, target_directory: str
    ) -> Any:

        vault_address = f"{org_name}/{vault_name}"
        urls = self._get_download_url(vault_address, version_or_tag).get('data', [])
        print(urls)
        df = pd.DataFrame(urls)
        full_tag = f"{org_name}/{vault_name}/{version_or_tag}"
        short_key = f"{org_name}/{vault_name}:{version_or_tag}"

        filtered_df1 = pd.DataFrame()
        filtered_df2 = pd.DataFrame()
        filtered_df3 = pd.DataFrame()

        if 'key' in df.columns:
            filtered_df1 = df[df['key'].str.contains(full_tag, na=False)].sort_values(
                by='lastModified', ascending=False
            )

        if 'shortKey' in df.columns:
            filtered_df2 = df[df['shortKey'].str.contains(short_key, na=False)].sort_values(
                by='lastModified', ascending=False
            )

        if 'tag' in df.columns:
            filtered_df3 = df[df['tag'] == version_or_tag].sort_values(by='lastModified', ascending=False)

        filtered_df = pd.concat([filtered_df1, filtered_df2, filtered_df3]).drop_duplicates()

        if filtered_df.empty:
            return f"Version {version_or_tag} not found"

        try:
            url_to_download = filtered_df.iloc[0]['url']
            downloaded_file_path = self.replace_path(full_tag, target_directory)
            self.download_file(url_to_download, downloaded_file_path)
            self.process_archive(downloaded_file_path, target_directory)
        except Exception as e:
            raise KaasCliException(f"Download {full_tag}:{version_or_tag} failed: {str(e)}") from e

        return f'Version {version_or_tag} downloaded to {target_directory}'

    def download_last_version(self, org_name: str, vault_name: str, target_directory: str) -> Any:
        vault_hash = self._vault or self._get_default_vault()
        if not vault_hash:
            return "Can't find default vault"

        urls = self._get_download_url(vault_hash)

        urls_data = urls.get('data', {})
        if not urls_data:
            return 'Something went wrong'

        latest_file = max(urls_data, key=lambda x: x['lastModified'])

        url = latest_file['url']
        key = latest_file['key'].split('/')[0]

        try:
            downloaded_file_path = self.replace_path(key, target_directory)
            self.download_file(url, downloaded_file_path)
            self.process_archive(downloaded_file_path, target_directory)
        except Exception:
            raise KaasCliException(f"Download {latest_file} failed") from None

        return f'Latest version of {latest_file} downloaded to {target_directory}'

    def process_archive(self, archive_path: str, extract_to: str) -> None:
        """
        Extracts files from an archive to a specified directory and then removes the archive.

        Args:
        archive_path (str): The path to the archive file.
        extract_to (str): The directory to extract the files to.
        """
        # Ensure the target directory exists
        os.makedirs(extract_to, exist_ok=True)

        # Extract the archive
        with ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        # Remove the archive file after extraction
        os.remove(archive_path)
        click.echo(f"Extracted archive to {extract_to}")

    def download_vault(self, target_directory: str) -> Any:
        vault_hash = self._vault or self._get_default_vault()
        if not vault_hash:
            return "Can't find default vault"

        urls = self._get_download_url(vault_hash)

        urls_data = urls.get('data', {})
        if not urls_data:
            return 'Something went wrong'

        for path in urls_data:
            url = urls_data[path]
            try:
                self.download_file(url, self.replace_path(path, target_directory))
            except Exception:
                raise KaasCliException(f"Download {path} failed") from None

        return f'{len(urls_data)} Files downloaded to {target_directory}'

    @staticmethod
    def _get_upload_data(file_list: list[Path], directory: Path) -> tuple[File_Data, Metadata]:
        data: File_Data = {}
        metadata = {}

        for file_path in file_list:
            file_uuid = str(uuid4())
            file_name_str = Path(file_path).relative_to(directory).as_posix()
            with file_path.open('rb') as file_object:
                data[f'file_{file_uuid}'] = (file_name_str, file_object.read(), None)
            updated_at = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
            # Ensure the file path is converted to a string
            metadata[file_uuid] = {'filename': file_name_str, 'updated_at': updated_at}

        data['metadata'] = (None, json.dumps(metadata), 'application/json')

        return data, metadata

    @staticmethod
    def _get_metadata(file_list: list[Path], directory: Path) -> Metadata:
        data, metadata = KaasClient._get_upload_data(file_list, Path(directory))
        return metadata

    def login(self) -> DeviceAuth:
        try:
            data = self._session.post(url=f'{self._url}{DEVICE_LOGIN_URL}')
        except Exception:
            raise KaasCliException("Login failed") from None
        return DeviceAuth(**data)

    def confirm_login(self, device_code: str) -> Confirmation:
        try:
            data = self._session.get(url=f'{self._url}{DEVICE_LOGIN_URL}', params={'device_code': device_code})
        except Exception:
            raise KaasCliException("Login failed") from None
        self._session = AuthenticatedSession(data['token'])
        self._save_session()
        return Confirmation(True)

    def check(self) -> Confirmation:
        data = self._session.get(url=f'{self._url}{USER_URL}')
        if data:
            return Confirmation(True)
        else:
            return Confirmation(False)

    def _get_download_url(self, vault_hash: str, tag: str | None = None) -> dict:
        query = f"?tag={tag}" if tag else ""
        org_name, vault_name = vault_hash.split('/')
        data = self._session.get(url=f'{self._url}{FILES_URL.format(org_name, vault_name)}{query}')
        return data

    def download_file(self, url: str, folder_path: str) -> None:
        file_path = Path(folder_path)

        file_path.parent.mkdir(parents=True, exist_ok=True)
        with requests.get(url, stream=True) as response:
            # Check if the request was successful
            response.raise_for_status()
            # Open a local file with write-binary mode in the specified folder
            with open(file_path, 'wb') as file:
                # Write the content of the response to the file in chunks
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

    def replace_path(self, input_string: str, target_directory: str) -> str:

        # Find the index of the first dash '/'
        dash_index = input_string.find('/')

        # Replace everything up to the first dash with 'test'
        result = target_directory + input_string[dash_index:]

        return result

    def read_new_files(self, files: list[str], target_directory: str) -> list[str]:
        new_files = []
        for file_name in files:
            file_path = Path(target_directory, file_name)
            if not file_path.exists():
                new_files.append(file_name)
        return new_files

    def pull_remote_files(self, files: list[str]) -> list[str]:
        try:
            data = self._session.get(url=f'{self._url}{FILES_LIST_URL}', params={'files': files})
        except Exception:
            raise KaasCliException("Pull remote files failed") from None
        return data

    def list_vaults(self) -> list[str]:
        try:
            data = self._session.get(url=f'{self._url}{VAULTS_ROOT_URL}')
        except Exception:
            raise KaasCliException("List vaults failed") from None
        return data

    def list_keys(self, vault: str) -> list[str]:
        try:
            data = self._session.get(url=f'{self._url}{VAULTS_KEY_URL.format(vault)}')['data']
        except Exception:
            raise KaasCliException("List vaults failed") from None
        return data

    def list_versions(self, vault: str) -> list[str]:
        try:
            data = self._get_download_url(vault)
        except Exception:
            raise KaasCliException("List vaults failed") from None
        return data['data']

    def logout(self) -> bool:
        """
        Log out the user by clearing the session and authentication token.
        Returns True if the logout was successful, False otherwise.
        """
        try:
            return self._remove_session()
        except Exception as e:
            logging.error(f"Logout failed: {e}")
            return False


QUERY_HELLO: Final = gql(
    """
    query Hello($name: String!) {
        hello(name: $name)
    }
    """
)
