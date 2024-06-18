"""CLI created with Typer."""
from bacore.domain import files, settings, system
from bacore.interactors import retrieve, verify
from rich import print
from pathlib import Path
from typer import Exit
from typing import Optional


class ProjectInfo:
    """ProjectInfo information."""

    def __init__(self, pyproject_file: Path):
        """Initialize."""
        self._pyproject_file_toml_object = files.TOML(path=pyproject_file)
        self._project_info_dict = retrieve.file_as_dict(file=self._pyproject_file_toml_object)
        self._project_info = settings.Project(name=self._project_info_dict["project"]["name"],
                                          version=self._project_info_dict["project"]["version"],
                                          description=self._project_info_dict["project"]["description"]
                                          )

    @property
    def name(self) -> str:
        """ProjectInfo name."""
        return self._project_info.name

    @property
    def version(self) -> Optional[str]:
        """ProjectInfo version."""
        return self._project_info.version

    @property
    def description(self) -> Optional[str]:
        """ProjectInfo description."""
        return self._project_info.description


def verify_programs_installed(list_of_programs: list[system.CommandLineProgram]):
    """Check if a list of command line programs are installed.

    TODO: This function does not follow the overall design of the project. -> Move to an interactor module.

    """
    programs_not_installed = 0

    for program in list_of_programs:
        if verify.command_on_path(program) is False:
            programs_not_installed += 1
            print(f'{program} is [red]not installed[/]. Install with: [blue]pip install bacore\\[cli\\][/]')

    if programs_not_installed > 0:
        raise Exit(code=1)
