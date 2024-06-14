import contextlib
import io
import os
import unittest.mock
import uuid

import mlflow.exceptions
import pytest

import mantik.runs.local
import mantik.utils.mantik_api.code_repository


@pytest.fixture()
def mock_get_code(mocker, sample_code_repository):
    mocker.patch(
        "mantik.utils.mantik_api.code_repository.get_one",
        return_value=sample_code_repository,
    )
    yield


@pytest.fixture()
def mock_get_experiment(mocker, sample_experiment_repository):
    mocker.patch(
        "mantik.utils.mantik_api.experiment_repository.get_one",
        return_value=sample_experiment_repository,
    )
    yield


@pytest.fixture()
def mock_get_unique_run_name(mocker, sample_run_configuration):
    mocker.patch(
        "mantik.utils.mantik_api.experiment_repository.get_unique_run_name",
        return_value=sample_run_configuration.name,
    )
    yield


@pytest.fixture()
def mock_update_run_status():
    with unittest.mock.patch(
        "mantik.utils.mantik_api.run.update_run_status",
    ) as patch:
        yield patch


@pytest.fixture()
def mock_update_run_logs():
    with unittest.mock.patch(
        "mantik.utils.mantik_api.run.update_logs",
    ) as patch:
        yield patch


@pytest.fixture()
def mock_keyboard_interrupt(mocker):
    mocker.patch("mlflow.run", side_effect=KeyboardInterrupt)
    yield


@pytest.fixture()
def mock_mlflow_execution_exception(mocker):
    mocker.patch(
        "mlflow.run",
        side_effect=mlflow.exceptions.ExecutionException(message="test"),
    )
    yield


@pytest.fixture()
def mock_mlflow_run(mocker):
    class Run:
        def get_status(self):
            return "FINISHED"

    mocker.patch("mlflow.run", return_value=Run())
    yield


@pytest.fixture()
def set_fake_mlflow_tracking():
    os.environ[mantik.utils.mlflow.TRACKING_TOKEN_ENV_VAR] = "FAKE TOKEN"
    os.environ[mantik.utils.mlflow.TRACKING_URI_ENV_VAR] = "mlruns"
    yield
    os.unsetenv(mantik.utils.mlflow.TRACKING_TOKEN_ENV_VAR)
    os.unsetenv(mantik.utils.mlflow.TRACKING_URI_ENV_VAR)


@pytest.mark.parametrize(
    ("run_output", "expected"),
    [
        (
            mantik.runs.local.LocalRunOutput(
                run_id=uuid.uuid4(), exception=None
            ),
            None,
        ),
        (
            mantik.runs.local.LocalRunOutput(
                run_id=uuid.uuid4(), exception=Exception()
            ),
            Exception,
        ),
    ],
)
def test_local_run(
    mock_get_code,
    mock_get_experiment,
    mock_get_unique_run_name,
    mock_update_run_logs,
    sample_run_configuration,
    sample_project_id,
    fake_token,
    run_output,
    expected,
) -> None:
    context = contextlib.nullcontext()
    if expected:
        context = pytest.raises(expected)
    with context:
        mocked_local_run_manager = unittest.mock.Mock(
            spec=mantik.runs.local.LocalRunManager
        )
        mocked_local_run_manager.start_local_run = unittest.mock.Mock(
            return_value=run_output
        )

        mantik.runs.local.run(
            data=sample_run_configuration,
            project_id=sample_project_id,
            mantik_token=fake_token,
            run_manager=mocked_local_run_manager,
        )

        mocked_local_run_manager.clone_git_repo.assert_called()
        mocked_local_run_manager.start_local_run.assert_called()


def test_path_directory_of_mlproject_file() -> None:
    assert (
        mantik.runs.local.path_directory_of_mlproject_file(
            "123/mlproject/MLProject"
        )
        == "123/mlproject"
    )


def test_submit_local_run_and_keyboard_interrupt(
    mock_mantik_api_request,
    sample_run_configuration,
    tmpdir,
    mock_update_run_status,
    mock_keyboard_interrupt,
    set_fake_mlflow_tracking,
) -> None:
    mocked_local_run_manager = mantik.runs.local.LocalRunManager()
    project_id = uuid.uuid4()
    run_id = uuid.uuid4()

    with mock_mantik_api_request(
        method="POST",
        end_point=f"/projects/" f"{str(project_id)}/runs?submit=False",
        status_code=201,
        json_response={"runId": str(run_id)},
    ):
        output = mocked_local_run_manager.start_local_run(
            mlflow_experiment_id=0,
            data=sample_run_configuration,
            mantik_token="access",
            project_id=project_id,
            uri=tmpdir,
        )
        assert isinstance(output.exception, KeyboardInterrupt)
    mlflow.end_run()
    assert mock_update_run_status.call_count == 2
    mock_update_run_status.assert_called_with(
        project_id=project_id, run_id=run_id, token="access", status="KILLED"
    )


def test_submit_local_run_and_execution_exception(
    mock_mantik_api_request,
    sample_run_configuration,
    tmpdir,
    mock_update_run_status,
    mock_mlflow_execution_exception,
    set_fake_mlflow_tracking,
) -> None:
    mocked_local_run_manager = mantik.runs.local.LocalRunManager()
    project_id = uuid.uuid4()
    run_id = uuid.uuid4()
    with mock_mantik_api_request(
        method="POST",
        end_point=f"/projects/" f"{str(project_id)}/runs?submit=False",
        status_code=201,
        json_response={"runId": str(run_id)},
    ):
        output = mocked_local_run_manager.start_local_run(
            mlflow_experiment_id=0,
            data=sample_run_configuration,
            mantik_token="access",
            project_id=project_id,
            uri=tmpdir,
        )
        assert isinstance(
            output.exception, mlflow.exceptions.ExecutionException
        )
    mlflow.end_run()
    assert mock_update_run_status.call_count == 2
    mock_update_run_status.assert_called_with(
        project_id=project_id, run_id=run_id, token="access", status="FAILED"
    )


def test_submit_local_run(
    mock_mantik_api_request,
    sample_run_configuration,
    tmpdir,
    mock_update_run_status,
    mock_mlflow_run,
    set_fake_mlflow_tracking,
) -> None:
    mocked_local_run_manager = mantik.runs.local.LocalRunManager()
    project_id = uuid.uuid4()
    run_id = uuid.uuid4()
    with mock_mantik_api_request(
        method="POST",
        end_point=f"/projects/" f"{str(project_id)}/runs?submit=False",
        status_code=201,
        json_response={"runId": str(run_id)},
    ):
        mocked_local_run_manager.start_local_run(
            mlflow_experiment_id=0,
            data=sample_run_configuration,
            mantik_token="access",
            project_id=project_id,
            uri=tmpdir,
        )
    mlflow.end_run()
    assert mock_update_run_status.call_count == 2
    mock_update_run_status.assert_called_with(
        project_id=project_id, run_id=run_id, token="access", status="FINISHED"
    )


class TestTee:
    def test_write_and_flush(self):
        stream_a = io.StringIO()
        stream_b = io.StringIO()
        tee = mantik.runs.local.Tee(stream_a, stream_b)
        message = "hello to both streams"
        tee.write(message)
        assert stream_a.getvalue() == message
        assert stream_b.getvalue() == message
        tee.flush()
        assert stream_a.read(256) == ""
        assert stream_b.read(256) == ""
