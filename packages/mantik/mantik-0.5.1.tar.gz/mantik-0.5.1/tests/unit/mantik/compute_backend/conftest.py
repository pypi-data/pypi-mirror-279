import pathlib

import pytest


@pytest.fixture(scope="session")
def mlproject_path() -> pathlib.Path:
    return (
        pathlib.Path(__file__).parent
        / "../../../../tests/resources/test-project"
    )
