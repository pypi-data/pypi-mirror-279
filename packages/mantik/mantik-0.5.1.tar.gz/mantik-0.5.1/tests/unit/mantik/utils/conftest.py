import pathlib

import pytest

import mantik.compute_backend as compute_backend

FILE_DIR = pathlib.Path(__file__).parent


@pytest.fixture(scope="function")
def example_unicore_config() -> compute_backend.config.core.Config:
    return compute_backend.config.core.Config(
        unicore_api_url="test-url",
        user="user",
        password="password",
        project="test-project",
        environment=compute_backend.config.environment.Environment(
            execution=compute_backend.config.executable.Apptainer(
                path=pathlib.Path("mantik-test.sif"),
            )
        ),
        resources=compute_backend.config.resources.Resources(queue="batch"),
        exclude=["*.sif"],
    )


@pytest.fixture()
def example_project_path() -> pathlib.Path:
    return FILE_DIR / "../../../resources/test-project"
