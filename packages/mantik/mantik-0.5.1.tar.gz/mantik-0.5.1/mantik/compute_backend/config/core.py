import dataclasses
import enum
import logging
import pathlib
import typing as t
import uuid

import mantik.compute_backend.config._base as _base
import mantik.compute_backend.config._utils as _utils
import mantik.compute_backend.config.environment as _environment
import mantik.compute_backend.config.exceptions as _exceptions
import mantik.compute_backend.config.firecrest as _firecrest
import mantik.compute_backend.config.read as read
import mantik.compute_backend.config.resources as _resources
import mantik.compute_backend.credentials as _credentials
import mantik.utils.env as env

COMPUTE_BUDGET_ACCOUNT_ENV_VAR = "MANTIK_COMPUTE_BUDGET_ACCOUNT"
_UNICORE_AUTH_SERVER_URL_ENV_VAR = "MANTIK_UNICORE_AUTH_SERVER_URL"
APPLICATION_LOGS_FILE = "mantik.log"

logger = logging.getLogger(__name__)


class SupportedBackends(enum.Enum):
    UNICORE = "unicore"
    FIRECREST = "firecrest"


@dataclasses.dataclass
class Config(_base.ConfigObject):
    """The backend config for the UNICORE MLflow backend."""

    user: str
    password: str
    project: str
    resources: _resources.Resources
    environment: t.Optional[_environment.Environment] = None
    exclude: t.Optional[t.List] = None
    unicore_api_url: t.Optional[str] = None
    firecrest: t.Optional[_firecrest.Firecrest] = None

    @classmethod
    def _from_dict(
        cls, config: t.Dict, connection_id: t.Optional[uuid.UUID] = None
    ) -> "Config":
        """

        Parameters
        ----------
        config : t.Dict
            the possible keys to specify inside the config dictionary are:
            REQUIRED:
                - UnicoreApiUrl : str
                    URL to the API of the UNICORE HPC used.

                The other required field MANTIK_USERNAME, MANTIK_PASSWORD
                and MANTIK_PROJECT are inferred from the environment.
            OPTIONAL:
                - Resources : dict
                    Dict of parameters specifying the resources
                    to request on the remote system.
                    More info can be found here:
                    https://sourceforge.net/p/unicore/wiki/Job_Description/
                - Environment : dict
                    Used to build a environment.Environment.
                - Exclude : list
                    List of files or file-patterns
                    that are not sent with the job


        Returns
        -------
        mantik.unicore._config.core.Config

        """
        (
            unicore_api_url,
            firecrest,
            credentials,
        ) = _get_unicore_or_firecrest_and_credentials(
            config=config,
            connection_id=connection_id,
        )
        project = env.get_required_env_var(COMPUTE_BUDGET_ACCOUNT_ENV_VAR)

        # Read remaining config sections.
        resources = _utils.get_required_config_value(
            name="Resources",
            value_type=_resources.Resources.from_dict,
            config=config,
        )
        environment = _utils.get_optional_config_value(
            name="Environment",
            value_type=_environment.Environment.from_dict,
            config=config,
        )
        exclude = _utils.get_optional_config_value(
            name="Exclude",
            value_type=list,
            config=config,
        )

        return cls(
            unicore_api_url=unicore_api_url,
            firecrest=firecrest,
            user=credentials.username,
            password=credentials.password,
            project=project,
            resources=resources,
            environment=environment,
            exclude=exclude,
        )

    def __post_init__(self):
        if self.environment is None:
            self.environment = _environment.Environment()

        # set SRUN_CPUS_PER_TASK to CPUsPerNode if not explicitly set
        self.environment = self.environment.set_srun_cpus_per_task_if_unset(
            self.resources
        )

        if self.firecrest is not None and (
            self.environment.pre_run_command_on_login_node is not None
            or self.environment.post_run_command_on_login_node is not None
        ):
            raise _exceptions.ConfigValidationError(
                "Pre-/PostRunCommandOnLoginNode not supported by firecREST"
            )

    @classmethod
    def from_filepath(
        cls, filepath: pathlib.Path, connection_id: t.Optional[uuid.UUID] = None
    ) -> "Config":
        """Initialize from a given file."""
        return cls._from_dict(
            read.read_config(filepath), connection_id=connection_id
        )

    @property
    def files_to_exclude(self) -> t.List[str]:
        return self.exclude or []

    def _to_dict(self) -> t.Dict:
        environment = (
            self.environment.to_dict() if self.environment is not None else {}
        )
        return {
            "Project": self.project,
            "Resources": self.resources,
            # Write stderr/stdout to given file to allow access to logs
            "Stdout": APPLICATION_LOGS_FILE,
            "Stderr": APPLICATION_LOGS_FILE,
            **environment,
        }

    def to_unicore_job_description(self, bash_script_name: str) -> t.Dict:
        """Convert to UNICORE job description."""
        environment = (
            self.environment.to_unicore_job_description(bash_script_name)
            if self.environment is not None
            else {}
        )
        return {
            **self.to_dict(),
            **environment,
        }

    def to_slurm_batch_script(
        self, arguments: str, run_id: str, run_dir: pathlib.Path
    ) -> str:
        """Create a Slurm batch script for firecREST.

        firecREST only allows to submit jobs via batch scripts, which has to be
        manually constructed.

        """
        return "\n".join(
            [
                "#!/bin/bash -l",
                f"#SBATCH --job-name='mantik-{run_id}'",
                self.resources.to_slurm_batch_script(),
                f"#SBATCH --output={run_dir}/mantik.log",
                f"#SBATCH --error={run_dir}/mantik.log",
                # The `--chdir` option is ignored by firecREST.
                # We could propose this feature, but for now we will
                # stick to manually changing the directory.
                'echo "firecREST working directory is $(pwd)"',
                'echo "Submitted batch script:"',
                "cat $(pwd)/script.batch",
                # _Must_ cd after cat, otherwise the `script.batch` file will
                # not be available.
                f'echo "Changing to Mantik run directory {run_dir}"',
                f"cd {run_dir}",
                self.environment.to_slurm_batch_script(
                    entry_point_arguments=arguments, run_dir=run_dir
                ),
            ]
        )

    def to_bash_script(self, arguments: str) -> str:
        """Create a bash script for UNICORE."""
        return self.environment.to_bash_script(arguments)

    def execution_environment_given(self) -> bool:
        return (
            self.environment is not None and self.environment.execution_given()
        )

    def add_env_vars(self, env_vars: t.Dict) -> None:
        self.environment.add_env_vars(env_vars)

    @property
    def backend_type(self) -> SupportedBackends:
        if self.unicore_api_url is not None:
            return SupportedBackends.UNICORE
        elif self.firecrest is not None:
            return SupportedBackends.FIRECREST
        else:
            raise NotImplementedError()


def _get_unicore_or_firecrest_and_credentials(
    config: t.Dict, connection_id: t.Optional[uuid.UUID] = None
) -> t.Tuple[
    t.Optional[str], t.Optional[_firecrest.Firecrest], _credentials.HpcRestApi
]:
    # Read UNICORE or firecREST info.
    unicore_api_url = _utils.get_optional_config_value(
        name="UnicoreApiUrl",
        value_type=str,
        config=config,
    )
    firecrest = _utils.get_optional_config_value(
        name="Firecrest",
        value_type=_firecrest.Firecrest.from_dict,
        config=config,
    )

    # Check that either UnicoreApiUrl or Firecrest section given
    if unicore_api_url is None and firecrest is None:
        raise _exceptions.ConfigValidationError(
            "Either UnicoreApiUrl or Firecrest details must be provided"
        )
    elif unicore_api_url is not None and firecrest is not None:
        raise _exceptions.ConfigValidationError(
            "Either UnicoreApiUrl or Firecrest details must be provided, "
            "but both are given"
        )

    # Read either UNICORE or firecREST credentials
    if unicore_api_url is not None:
        credentials = _credentials.HpcRestApi.from_unicore_env_vars(
            connection_id
        )
    elif firecrest is not None:
        credentials = _credentials.HpcRestApi.from_firecrest_env_vars(
            connection_id
        )
    else:
        raise RuntimeError("Neither UnicoreApiUrl nor Firecrest section given")

    return unicore_api_url, firecrest, credentials


def backend_type_from_dict(backend_config: t.Dict):
    if "UnicoreApiUrl" in backend_config and "Firecrest" not in backend_config:
        return SupportedBackends.UNICORE
    elif (
        "Firecrest" in backend_config and "UnicoreApiUrl" not in backend_config
    ):
        return SupportedBackends.FIRECREST
    else:
        raise _exceptions.ConfigValidationError(
            "Either UnicoreApiUrl or Firecrest details must be provided"
        )
