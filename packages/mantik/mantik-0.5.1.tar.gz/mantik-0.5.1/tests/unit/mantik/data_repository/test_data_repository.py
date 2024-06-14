import os
import pathlib
import unittest.mock
import uuid

import pytest
import responses

import mantik.cli.data
import mantik.data_repository.data_repository
import mantik.utils.mantik_api.client as mantik_api

FAKE_API_URL = "https://fake.com"


@pytest.fixture(scope="session")
def sample_project_uuid():
    return uuid.uuid4()


@pytest.fixture(scope="session")
def sample_data_repository_uuid():
    return uuid.uuid4()


@pytest.fixture(scope="session")
def sample_connection_uuid():
    return uuid.uuid4()


@pytest.fixture(scope="session")
def sample_target_dir() -> pathlib.Path:
    return pathlib.Path("/sample/target/dir")


@pytest.fixture(scope="function")
def sample_version() -> str:
    return "1234"


@pytest.fixture(scope="session")
def fake_user_id_str():
    return str(uuid.uuid4())


@pytest.fixture
def mock_mantik_api_url():
    os.environ[mantik_api._MANTIK_API_URL_ENV_VAR] = FAKE_API_URL
    yield
    os.unsetenv(mantik_api._MANTIK_API_URL_ENV_VAR)


@pytest.fixture
def mock_data_repository_response_with_dvc(
    sample_project_uuid,
    sample_data_repository_uuid,
    sample_version,
    sample_connection_uuid,
    mock_mantik_api_url,
):
    responses.add(
        responses.GET,
        url=f"{FAKE_API_URL}/projects/{str(sample_project_uuid)}/data"
        f"/{str(sample_data_repository_uuid)}",
        status=200,
        json={
            "uri": "fake.com",
            "isDvcEnabled": True,
            "dvcConnectionId": str(sample_connection_uuid),
            "versions": {sample_version: "fake-commit-hash"},
        },
    )
    yield


@pytest.fixture
def mock_data_repository_response_without_dvc(
    sample_project_uuid,
    sample_data_repository_uuid,
    sample_version,
    mock_mantik_api_url,
):
    responses.add(
        responses.GET,
        url=f"{FAKE_API_URL}/projects/{str(sample_project_uuid)}/data"
        f"/{str(sample_data_repository_uuid)}",
        status=200,
        json={
            "uri": "fake.com",
            "isDvcEnabled": False,
            "dvcConnectionId": None,
            "versions": {sample_version: "fake-commit-hash"},
        },
    )
    yield


@pytest.fixture
def mock_connection_response(
    sample_project_uuid,
    fake_user_id_str,
    sample_connection_uuid,
    mock_mantik_api_url,
):
    responses.add(
        responses.GET,
        url=f"{FAKE_API_URL}/users/{fake_user_id_str}/settings/"
        f"connections/{str(sample_connection_uuid)}",
        status=200,
        json={
            "connectionId": str(sample_connection_uuid),
            "user": {"userId": fake_user_id_str, "name": "Kiwi"},
            "connectionName": "KiwiConnection",
            "connectionProvider": "S3",
            "authMethod": "Username-Password",
            "loginName": "access-key",
            "password": "secret-access-key",
            "token": "token",
        },
    )
    yield


@pytest.fixture()
def mock_user_id_from_token(fake_user_id_str):
    with unittest.mock.patch(
        "tokens.jwt.get_user_id_from_token", return_value=fake_user_id_str
    ):
        yield


@responses.activate
def test_download_data_repository_without_dvc(
    sample_project_uuid,
    sample_data_repository_uuid,
    sample_target_dir,
    sample_version,
    mock_data_repository_response_without_dvc,
):
    with unittest.mock.patch(
        "mantik.data_repository.data_repository.git_clone_with_commit_hash"
    ) as mocked_git_clone_function, unittest.mock.patch(
        "mantik.data_repository.data_repository.dvc_pull_with_aws_credentials"
    ) as mocked_dvc_pull_with_aws_credentials_function:
        mantik.data_repository.data_repository.download_data_repository(
            project_id=sample_project_uuid,
            data_repository_id=sample_data_repository_uuid,
            version=sample_version,
            target_dir=sample_target_dir,
            token="1234",
        )

        mocked_git_clone_function.assert_called()
        mocked_dvc_pull_with_aws_credentials_function.assert_not_called()


@responses.activate
def test_download_data_repository_with_dvc(
    sample_project_uuid,
    sample_data_repository_uuid,
    sample_target_dir,
    sample_version,
    mock_connection_response,
    mock_data_repository_response_with_dvc,
    mock_user_id_from_token,
):
    with unittest.mock.patch(
        "mantik.data_repository.data_repository.git_clone_with_commit_hash"
    ) as mocked_git_clone_function, unittest.mock.patch(
        "mantik.data_repository.data_repository.dvc_pull_with_aws_credentials"
    ) as mocked_dvc_pull_with_aws_credentials_function:
        mantik.data_repository.data_repository.download_data_repository(
            project_id=sample_project_uuid,
            data_repository_id=sample_data_repository_uuid,
            version=sample_version,
            target_dir=sample_target_dir,
            token="1234",
        )

        mocked_git_clone_function.assert_called()
        mocked_dvc_pull_with_aws_credentials_function.assert_called()
