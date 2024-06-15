from __future__ import annotations

from typing import TYPE_CHECKING

import click

from kaas_cli import __version__

from .client import KaasClient
from .config import DEFAULT_DIRECTORY, DEFAULT_TOKEN, SERVER_URL, CustomHelpOption

if TYPE_CHECKING:
    from click.core import Context


@click.group()
@click.version_option(version=__version__, prog_name='kaas-cli')
@click.pass_context
def cli(
    ctx: Context,
) -> None:
    """KaaS Command Line Interface"""
    ctx.ensure_object(dict)
    ctx.obj["client"] = KaasClient(
        url=SERVER_URL,
    )


@cli.command(
    cls=CustomHelpOption,
    help="Upload proofs to the remote server. VAULT_SPEC should be in the format <ORG_NAME>/<VAULT_NAME>:<TAG>",
)
@click.argument('vault_spec', required=True)
@click.option(
    "-d",
    "--directory",
    default=DEFAULT_DIRECTORY,
    show_default=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Directory containing proofs to upload",
)
@click.option("--url", "-u", required=False, default=SERVER_URL, show_default=True, help="Server URL")
@click.option("--token", "-t", required=False, default=DEFAULT_TOKEN, help="Personal access key for vault")
@click.option("--tag", required=False, help="Tag of the version to upload")
@click.pass_context
def upload(ctx: Context, vault_spec: str, directory: str, url: str, token: str | None, tag: str | None) -> None:
    try:
        org_name, vault_and_tag = vault_spec.split('/')
        vault_name, tag_name = vault_and_tag.split(':')
    except ValueError:
        click.echo("Invalid vault specification. Use the format orgName/vaultName:tag")
        return

    ctx.ensure_object(dict)
    client: KaasClient = KaasClient(url=url, token=token, vault=vault_name, org=org_name)
    ctx.obj["client"] = client
    response_message = client.upload_files_s3(directory=directory, tag=tag_name or tag)
    click.echo(response_message)


@cli.command(
    cls=CustomHelpOption,
    help="Download proofs from the remote server. VAULT_SPEC should be in the format <ORG_NAME>/<VAULT_NAME>:<TAG>",
)
@click.argument("vault_spec", required=False)
@click.option(
    "-d",
    "--directory",
    default=DEFAULT_DIRECTORY,
    show_default=True,
    type=click.Path(exists=False, file_okay=False, dir_okay=True),
    help="Directory to save downloaded proofs",
)
@click.option("--url", "-u", default=SERVER_URL, show_default=True, help="Server URL")
@click.option("--token", "-t", default=DEFAULT_TOKEN, help="Personal access key for vault")
@click.pass_context
def download(
    ctx: Context,
    vault_spec: str,
    directory: str,
    url: str,
    token: str | None,
) -> None:
    try:
        org_name, vault_and_tag = vault_spec.split('/')
        vault_name, tag_name_or_file_name = vault_and_tag.split(':')
    except ValueError:
        click.echo("Invalid vault specification. Use the format orgName/vaultName:tag")
        return None

    if not org_name or not vault_name:
        click.echo("Invalid vault specification. Use the format orgName/vaultName:tag")
        return None
    ctx.ensure_object(dict)
    client: KaasClient = KaasClient(url=url, token=token, vault=vault_name, org=org_name)
    ctx.obj["client"] = client
    if not tag_name_or_file_name:
        message = client.download_last_version(org_name, vault_name, target_directory=directory)
        click.echo(message)
        return None

    try:
        message = client.download_version_or_tag(
            org_name, vault_name, tag_name_or_file_name, target_directory=directory
        )
        click.echo(message)
        return None
    except ValueError:
        click.echo("Invalid vault specification. Use the format orgName/vaultName:tag")
        return None


@cli.command(cls=CustomHelpOption, help="Say hello.")
@click.option("-n", "--name", default="World", show_default=True, help="Name to say hello to")
@click.pass_context
def hello(ctx: Context, name: str) -> None:
    client: KaasClient = ctx.obj["client"]

    response = client.hello(name=name)
    click.echo(response)


@cli.command(cls=CustomHelpOption, help="Login to the system.")
@click.pass_context
def login(ctx: Context) -> None:
    client: KaasClient = ctx.obj["client"]
    data = client.login()
    click.echo(f"Your user code: {data.user_code}")
    click.echo(f"Open the link and type your code {data.verification_uri}")
    click.echo("Then hit 'enter'")
    input_value = click.prompt("Press Enter to continue or type 'q' to quit", default="", show_default=False)
    if input_value.lower() == 'q':
        click.echo("You left authentication")
        return
    click.echo("You pressed Enter. The application continues...")
    confirm_success = client.confirm_login(data.device_code).success
    if not confirm_success:
        click.echo("Authentication failed")
        return
    click.echo("Access token received. We store it in cache folder")


@cli.command(cls=CustomHelpOption, help="List local proofs.", aliases=['l', 'ls'])
@click.option(
    "-d",
    "--directory",
    default=DEFAULT_DIRECTORY,
    show_default=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Directory to list local proofs",
)
@click.option("--remote", is_flag=True, help="List remote proofs instead of local proofs", default=False)
@click.pass_context
def list(ctx: Context, directory: str = DEFAULT_DIRECTORY, remote: bool = False) -> None:
    client: KaasClient = ctx.obj["client"]
    if remote:
        proofs = client.list_remote()
    else:
        proofs = client.list_local_proofs(directory=directory)
    if not proofs:
        click.echo('No proofs found')
    for proof in proofs:
        click.echo(proof)


def list_remote(ctx: Context) -> None:
    client: KaasClient = ctx.obj["client"]
    proofs = client.list_remote()
    for proof in proofs:
        click.echo(proof)


@cli.command(cls=CustomHelpOption, name="check-auth", help="Check authentication status.")
@click.pass_context
def check_auth(ctx: Context) -> None:
    client: KaasClient = ctx.obj["client"]
    error_message = f"Authentication failed, please use {click.style('--token', fg='red')} flag or {click.style('kaas-cli login', fg='red')} to authenticate."
    try:
        is_authenticated = client.check()
        if is_authenticated:
            click.echo("You are currently authenticated.")
        else:
            click.echo(error_message)
    except Exception:
        click.echo(error_message)


@cli.command(cls=CustomHelpOption, name="logout", help="Log out from the system.")
@click.pass_context
def logout(ctx: Context) -> None:
    client: KaasClient = ctx.obj["client"]
    logout_success = client.logout()
    if logout_success:
        click.echo("You have been logged out successfully.")
    else:
        click.echo("Logout failed. You may not be logged in.")
