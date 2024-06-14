import logging
import os
import pathlib
import subprocess
import typing as t
import uuid

import git

import mantik.utils.mantik_api.connection
import mantik.utils.mantik_api.data_repository
import tokens

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def download_data_repository(
    project_id: uuid.UUID,
    data_repository_id: uuid.UUID,
    version: t.Optional[str],
    target_dir: pathlib.Path,
    token: str,
) -> str:
    """Downloads a GIT based data repository, along with its DVC files."""

    data_repository_details = mantik.utils.mantik_api.data_repository.get_one(
        project_id=project_id,
        data_repository_id=data_repository_id,
        token=token,
    )
    try:
        desired_git_commit_hash = (
            data_repository_details.versions[version] if version else None
        )
    except KeyError:
        raise ValueError(
            f"Invalid version '{version}' specified. Available "
            f"data versions: '{list(data_repository_details.versions.keys())}'"
        )

    git_clone_with_commit_hash(
        git_uri=data_repository_details.uri,
        git_commit_hash=desired_git_commit_hash,
        target_dir=target_dir,
    )

    if not data_repository_details.is_dvc_enabled:
        return f"Cloned to {target_dir}"

    connection = mantik.utils.mantik_api.connection.get(
        user_id=uuid.UUID(tokens.jwt.get_user_id_from_token(token)),
        connection_id=data_repository_details.dvc_connection_id,
        token=token,
    )

    if connection.connection_provider == "S3":
        dvc_pull_with_aws_credentials(
            aws_access_key_id=connection.login_name,
            aws_secret_access_key=connection.password,
            target_dir=target_dir,
        )
    else:
        raise ValueError(
            "Connection provider not supported by our DVC backend."
        )

    return f"Cloned to {target_dir} with DVC"


def git_clone_with_commit_hash(
    git_uri: str, git_commit_hash: str, target_dir: pathlib.Path
):
    """Make target folder, git clone, and checkout a specific commit."""

    # clone the git repository
    logger.info("Cloning the git data repository...")
    target_dir.mkdir(parents=True, exist_ok=True)
    repo = git.Repo.clone_from(git_uri, target_dir)

    # checkout desired version
    if git_commit_hash:
        os.chdir(target_dir)
        repo.git.checkout(git_commit_hash)


def dvc_pull_with_aws_credentials(
    aws_access_key_id: str,
    aws_secret_access_key: str,
    target_dir: t.Optional[pathlib.Path] = None,
):
    """Perform DVC pull using S3 as a DVC backend"""
    verify_dvc_is_installed()
    if target_dir:
        os.chdir(target_dir)

    logger.info("Pulling files from the DVC backend...")
    subprocess.run(
        ["dvc", "pull"],
        env={
            "PATH": os.environ["PATH"],
            "AWS_ACCESS_KEY_ID": aws_access_key_id,
            "AWS_SECRET_ACCESS_KEY": aws_secret_access_key,
        },
    )


def verify_dvc_is_installed():
    try:
        logger.info("Verifying dvc installation...")
        subprocess.run(["dvc", "--version"])
    except FileNotFoundError:
        raise RuntimeError(
            "DVC is not installed. Please refer to https://dvc.org/doc/install"
        )
    else:
        logger.info("DVC is installed.")
