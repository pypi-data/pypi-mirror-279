"""Top level conftest.py for BACore test cases."""
import pytest


@pytest.fixture
def fixture_pyproject_file(tmp_path):
    """Create a temporary pyproject.toml file."""
    toml_content = """
    [project]
    name = 'bacore'
    version = "1.0.0"
    description = "BACore is a framework for business analysis and test automation."
    """
    file = tmp_path / "pyproject.toml"
    file.write_text(toml_content)
    return file
