import uuid

import mantik.utils.mantik_api as mantik_api


def test_submit_run(mock_mantik_api_request, info_caplog):
    submit_run_data = {
        "name": "run-name",
        "experimentRepositoryId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "codeRepositoryId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "branch": "main",
        "commit": "string",
        "dataRepositoryId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "connectionId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "computeBudgetAccount": "a-budget-account",
        "mlflowMlprojectFilePath": "/path",
        "entryPoint": "main",
        "mlflowParameters": {},
        "backendConfig": {
            "UnicoreApiUrl": "https://zam2125.zam.kfa-juelich.de:9112/JUWELS/rest/core",  # noqa F401
            "Environment": {
                "Apptainer": {"Path": "some/image/path.name", "Type": "local"}
            },
            "Resources": {"Queue": "devel", "Nodes": 1},
        },
    }
    project_id = uuid.uuid4()
    with mock_mantik_api_request(
        method="POST",
        end_point=f"/projects/{project_id}/runs",
        status_code=201,
        json_response={},
        expected_error=204,
    ) as (m, error):
        mantik_api.run.submit_run(
            project_id=project_id,
            submit_run_data=submit_run_data,
            token="test_token",
        )
        assert any(
            "Run has been successfully submitted" in message
            for message in info_caplog.messages
        )
    if error:
        assert any(
            "Call to Mantik API" in message for message in info_caplog.messages
        )


def test_save_run(mock_mantik_api_request, info_caplog):
    project_id = uuid.uuid4()
    with mock_mantik_api_request(
        method="POST",
        end_point=f"/projects/{project_id}/runs",
        status_code=201,
        json_response={},
        expected_error=204,
    ) as (m, error):
        mantik_api.run.save_run(
            project_id=project_id,
            run_data={},
            token="test_token",
        )
        assert any(
            "Run has been successfully saved" in message
            for message in info_caplog.messages
        )


def test_update_run_status(mock_mantik_api_request, info_caplog):
    project_id = uuid.uuid4()
    run_id = uuid.uuid4()
    with mock_mantik_api_request(
        method="PUT",
        end_point=f"/projects/{project_id}/runs/{run_id}/status",
        status_code=200,
        json_response={},
        expected_error=204,
    ) as (m, error):
        mantik_api.run.update_run_status(
            project_id=project_id,
            status="FINISHED",
            token="test_token",
            run_id=run_id,
        )
        assert any(
            "Run status has been successfully updated" in message
            for message in info_caplog.messages
        )


def test_update_logs(mock_mantik_api_request, info_caplog):
    project_id = uuid.uuid4()
    run_id = uuid.uuid4()
    with mock_mantik_api_request(
        method="PUT",
        end_point=f"/projects/{project_id}/runs/{run_id}/logs",
        status_code=200,
        json_response={},
        expected_error=204,
    ) as (m, error):
        mantik_api.run.update_logs(
            project_id=project_id,
            logs="Test \n logs",
            token="test_token",
            run_id=run_id,
        )
        assert any(
            "Run logs has been successfully updated" in message
            for message in info_caplog.messages
        )


def test_get_download_artifact_url(mock_mantik_api_request, info_caplog):
    project_id = uuid.uuid4()
    run_id = uuid.uuid4()
    download_url = "test-url"
    with mock_mantik_api_request(
        method="GET",
        end_point=f"/projects/{project_id}/runs/{run_id}/artifacts",
        status_code=200,
        json_response={"url": download_url},
        expected_error=204,
    ) as (m, error):
        url = mantik_api.run.get_download_artifact_url(
            project_id=project_id,
            token="test_token",
            run_id=run_id,
        )
        assert url == download_url
        assert any(
            "Artifacts' download url successfully fetched" in message
            for message in info_caplog.messages
        )
