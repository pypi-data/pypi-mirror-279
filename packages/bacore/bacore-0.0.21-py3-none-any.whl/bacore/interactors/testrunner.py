"""Testrunner Interactor Module."""
from bacore.domain import settings


class TestRunner:
    """Test runner with pytest."""

    def __init__(self, project_info: settings.Project):
        """Initialize."""
        self._project_info = project_info

    def run(self):
        """Run tests."""
        print(f"Running tests for project: [blue]{self._project_info.name}[/].")


