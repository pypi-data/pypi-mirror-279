import io
import pathlib
import unittest
import uuid
import zipfile

import pytest

import mantik.runs.schemas as run_schemas
import mantik.utils.mantik_api.code_repository as code_api
import mantik.utils.mantik_api.experiment_repository as experiment_api


@pytest.fixture(scope="session")
def sample_experiment_repository_id():
    return uuid.uuid4()


@pytest.fixture(scope="session")
def sample_code_repository_id():
    return uuid.uuid4()


@pytest.fixture(scope="session")
def sample_project_id() -> uuid.UUID:
    return uuid.uuid4()


@pytest.fixture()
def sample_experiment_repository(sample_experiment_repository_id):
    return experiment_api.ExperimentRepository(
        experiment_repository_id=sample_experiment_repository_id,
        mlflow_experiment_id="123",
        name="Name",
        artifact_location="somewhere.com",
    )


@pytest.fixture()
def sample_code_repository(sample_code_repository_id):
    return code_api.CodeRepository(
        code_repository_id=sample_code_repository_id,
        code_repository_name="Name",
        uri="some/uri.git",
        access_token="1234",
    )


@pytest.fixture(scope="session")
def sample_run_configuration(
    sample_experiment_repository_id, sample_code_repository_id
) -> run_schemas.RunConfiguration:
    return run_schemas.RunConfiguration(
        name="Sample",
        experiment_repository_id=sample_experiment_repository_id,
        code_repository_id=sample_code_repository_id,
        branch="branch",
        commit="commit",
        data_repository_id=uuid.uuid4(),
        mlflow_mlproject_file_path="some/path/MLProject",
        entry_point="main",
        mlflow_parameters={"output": "hello world"},
        backend_config={},
    )


@pytest.fixture()
def fake_token():
    return "1234"


@pytest.fixture
def resource():
    return (
        pathlib.Path(__file__).parent.parent.parent
        / "resources/test-project/MLproject"
    )


@pytest.fixture
def mock_get_artifacts_url():
    yield unittest.mock.patch(
        "mantik.utils.mantik_api.run.get_download_artifact_url",
        return_value="https://fake/url/artifacts.zip?yada&&yada",
    )


@pytest.fixture
def zipped_file_name():
    return "test_file_name"


@pytest.fixture
def zipped_file_bytes(tmpdir, zipped_file_name, resource):
    def create_zip(input_file, output_zip):
        with zipfile.ZipFile(output_zip, "w") as zipf:
            zipf.write(input_file)
        with open(output_zip, "rb") as zip_file:
            byte_stream = io.BytesIO(zip_file.read())
        return byte_stream

    return create_zip(resource, tmpdir / zipped_file_name)


@pytest.fixture
def mock_get_url(zipped_file_bytes):
    yield unittest.mock.patch("requests.get", return_value=zipped_file_bytes)


@pytest.fixture
def mock_authentication():
    with unittest.mock.patch(
        "mantik.authentication.auth.get_valid_access_token",
        return_value="1234-token",
    ):
        yield "1234-token"
