import logging
import pathlib
import typing as t
import uuid

import click

import mantik.cli._options as main_options
import mantik.cli.runs._options as _options
import mantik.cli.runs.runs as runs
import mantik.cli.utils as utils
import mantik.compute_backend.config.core as core
import mantik.compute_backend.config.read as read
import mantik.utils.mantik_api as mantik_api

logger = logging.getLogger(__name__)


@runs.cli.command("submit")
@_options.MLPROJECT_PATH
@main_options.get_name_option(required=True, help_option="Name of the Run.")
@_options.ENTRY_POINT
@click.option(
    "--backend-config",
    type=click.Path(dir_okay=False, path_type=pathlib.Path),
    required=True,
    help="Relative or absolute path to backend config file.",
)
@main_options.PROJECT_ID
@main_options.DATA_REPOSITORY_ID
@main_options.EXPERIMENT_REPOSITORY_ID
@main_options.CODE_REPOSITORY_ID
@_options.BRANCH
@_options.COMMIT
@click.option(
    "--compute-budget-account",
    type=str,
    default=None,
    help=f"""Name of your Compute Budget Account on HPC

        If not specified, it is inferred from the environment variable
        {core.COMPUTE_BUDGET_ACCOUNT_ENV_VAR}.

    """,
    envvar=core.COMPUTE_BUDGET_ACCOUNT_ENV_VAR,
)
@_options.PARAMETER
@main_options.VERBOSE
@main_options.get_connection_id(required=True)
def run_project(
    name: str,
    mlproject_path: pathlib.Path,
    entry_point: str,
    backend_config: pathlib.Path,
    parameter: t.List[str],
    verbose: bool,  # noqa
    project_id: t.Optional[uuid.UUID],
    data_repository_id: t.Optional[uuid.UUID],
    experiment_repository_id: t.Optional[uuid.UUID],
    code_repository_id: t.Optional[uuid.UUID],
    branch: t.Optional[str],
    commit: t.Optional[str],
    compute_budget_account: t.Optional[str],
    connection_id: t.Optional[uuid.UUID],
) -> None:
    """Submit an MLflow project as a run to the Mantik Compute Backend.

    Note that `MLPROJECT_PATH` is the relative path to the MLflow project
    folder with your Code Repository as root.

    Remember that when you submit a run, the code is retrieved from your
    remote Git Code Repository. So make sure to commit and push your
    changes before submitting a run! The only file read from your local
    system is the backend config.

    To find the respective required IDs make sure to check Mantik's UI

    """
    _options.check_commit_or_branch(branch=branch, commit=commit, logger=logger)

    logger.debug("Parsing MLflow entry point parameters")
    parameters = utils.dict_from_list(parameter)

    config = read.read_config(backend_config)
    data = {
        "name": name,
        "experimentRepositoryId": str(experiment_repository_id),
        "codeRepositoryId": str(code_repository_id),
        "branch": branch,
        "commit": commit,
        "dataRepositoryId": str(data_repository_id)
        if data_repository_id is not None
        else None,
        "connectionId": str(connection_id),
        "computeBudgetAccount": compute_budget_account,
        "mlflowMlprojectFilePath": mlproject_path.as_posix(),
        "entryPoint": entry_point,
        "mlflowParameters": parameters,
        "backendConfig": config,
    }
    token = utils.access_token_from_env_vars()
    response = mantik_api.run.submit_run(
        project_id=project_id, submit_run_data=data, token=token
    )
    click.echo(response.content)
