import pytest
import os


@pytest.fixture
def instructions_from_filename(request: pytest.FixtureRequest) -> str:
    """Reads file based on filename found in **tests/fixtures**

    Args:
        request (pytest.FixtureRequest): Name of the file to be read

    Returns:
        list[str]: List of stripped lines
    """
    filename = request.param
    file_path = os.path.join("tests", "fixtures", filename)
    with open(file_path, "r") as f:
        return f.read()
