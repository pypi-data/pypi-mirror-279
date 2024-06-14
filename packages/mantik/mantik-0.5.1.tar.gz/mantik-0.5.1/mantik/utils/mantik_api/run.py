import logging
import uuid

import mantik.utils.mantik_api.client as client

logger = logging.getLogger(__name__)


def submit_run(project_id: uuid.UUID, submit_run_data: dict, token: str):
    endpoint = f"/projects/{project_id}/runs"
    response = client.send_request_to_mantik_api(
        method="POST", data=submit_run_data, url_endpoint=endpoint, token=token
    )
    logger.info("Run has been successfully submitted")
    return response


def save_run(project_id: uuid.UUID, run_data: dict, token: str):
    endpoint = f"/projects/{project_id}/runs"
    response = client.send_request_to_mantik_api(
        method="POST",
        data=run_data,
        url_endpoint=endpoint,
        token=token,
        query_params={"submit": False},
    )
    logger.info("Run has been successfully saved")
    return response


def update_run_status(
    project_id: uuid.UUID, run_id: uuid.UUID, status: str, token: str
):
    endpoint = f"/projects/{project_id}/runs/{run_id}/status"
    response = client.send_request_to_mantik_api(
        method="PUT", data=status, url_endpoint=endpoint, token=token
    )
    logger.info("Run status has been successfully updated")
    return response


def update_logs(
    project_id: uuid.UUID, run_id: uuid.UUID, logs: str, token: str
):
    endpoint = f"/projects/{project_id}/runs/{run_id}/logs"
    response = client.send_request_to_mantik_api(
        method="PUT", data=logs, url_endpoint=endpoint, token=token
    )
    logger.info("Run logs has been successfully updated")
    return response


def get_download_artifact_url(
    project_id: uuid.UUID, run_id: uuid.UUID, token: str
):
    endpoint = f"/projects/{project_id}/runs/{run_id}/artifacts"
    response = client.send_request_to_mantik_api(
        method="GET", data={}, url_endpoint=endpoint, token=token
    )
    logger.info("Artifacts' download url successfully fetched")
    return response.json()["url"]
