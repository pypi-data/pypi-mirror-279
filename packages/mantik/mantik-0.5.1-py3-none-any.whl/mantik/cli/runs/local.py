import logging
import pathlib
import platform
import typing as t
import uuid

import click

import mantik.cli._options as main_options
import mantik.cli.runs._options as _options
import mantik.cli.runs.runs as runs
import mantik.cli.utils as utils
import mantik.runs.local as local_runs
import mantik.runs.schemas as schemas


logger = logging.getLogger(__name__)


def get_gpu_info() -> list:
    import GPUtil

    gpus = GPUtil.getGPUs()

    gpu_info_list = []

    for gpu in gpus:
        gpu_info = {
            "Name": gpu.name,
            "ID": str(gpu.id),
            "Driver": gpu.driver,
            "TotalMemory": str(gpu.memoryTotal),
        }

        gpu_info_list.append(gpu_info)

    return gpu_info_list


def get_system_details() -> dict:
    import cpuinfo
    import psutil

    system_details = {
        "Platform": platform.platform(),
        "CpuModel": cpuinfo.get_cpu_info().get("brand_raw"),
        "CpuCoreCount": psutil.cpu_count(),
        "TotalMemoryGB": psutil.virtual_memory().total / (1024**3),
        "GPUInfo": get_gpu_info(),
    }
    return {"SystemDetails": system_details}


@runs.cli.command("local")
@_options.MLPROJECT_PATH
@main_options.get_name_option(required=True, help_option="Name of the Run.")
@_options.ENTRY_POINT
@main_options.PROJECT_ID
@main_options.DATA_REPOSITORY_ID
@main_options.EXPERIMENT_REPOSITORY_ID
@main_options.CODE_REPOSITORY_ID
@_options.BRANCH
@_options.COMMIT
@click.option(
    "--backend-config-system-info",
    type=bool,
    default=True,
    help="Populate the backend config JSON with system info.",
)
@_options.PARAMETER
@main_options.VERBOSE
def run_project(
    name: str,
    mlproject_path: pathlib.Path,
    entry_point: str,
    parameter: t.List[str],
    verbose: bool,  # noqa
    project_id: uuid.UUID,
    data_repository_id: t.Optional[uuid.UUID],
    experiment_repository_id: uuid.UUID,
    code_repository_id: uuid.UUID,
    branch: t.Optional[str],
    commit: t.Optional[str],
    backend_config_system_info: bool,
) -> None:
    """Run an MLflow project locally and save the results in Mantik API

    Note that `MLPROJECT_PATH` is the relative path to the MLflow project file
    with your Code Repository as root.

    Remember that when you execute a run, the code is retrieved from your
    remote Git Code Repository. So make sure to commit and push your
    changes before executing a run!

    To find the respective required IDs make sure to check Mantik's UI

    """

    _options.check_commit_or_branch(branch=branch, commit=commit, logger=logger)

    logger.debug("Parsing MLflow entry point parameters")
    parameters = utils.dict_from_list(parameter)

    mantik_token = utils.access_token_from_env_vars()

    system_details = get_system_details() if backend_config_system_info else {}
    local_runs.run(
        data=schemas.RunConfiguration(
            name=name,
            experiment_repository_id=experiment_repository_id,
            code_repository_id=code_repository_id,
            branch=branch,
            commit=commit,
            data_repository_id=data_repository_id,
            mlflow_mlproject_file_path=mlproject_path.as_posix(),
            entry_point=entry_point,
            mlflow_parameters=parameters,
            backend_config=system_details,
        ),
        project_id=project_id,
        mantik_token=mantik_token,
    )
    click.echo("Done!")
