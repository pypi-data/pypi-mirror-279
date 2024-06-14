import pathlib
import typing as t
import uuid

import click

import mantik.cli._options as _options
import mantik.cli.main as main
import mantik.cli.utils as cli_utils
import mantik.data_repository.data_repository as data_repository

GROUP_NAME = "data"


@main.cli.group(GROUP_NAME)
def cli() -> None:
    """Interaction with data through the mantik api."""


@cli.command("fetch")
@_options.PROJECT_ID
@_options.DATA_REPOSITORY_ID
@click.option(
    "--version",
    required=False,
    type=str,
    help="Version to checkout. Defaults to newest.",
)
@_options.get_target_dir_option_required(
    help_option="Path to directory where the data will be stored.",
)
def download_data_repository(
    project_id: uuid.UUID,
    data_repository_id: uuid.UUID,
    version: t.Optional[str],
    target_dir: str,
) -> None:
    """Download data repository."""
    output = data_repository.download_data_repository(
        project_id=project_id,
        data_repository_id=data_repository_id,
        version=version,
        target_dir=pathlib.Path(target_dir),
        token=cli_utils.access_token_from_env_vars(),
    )
    click.echo(output)
