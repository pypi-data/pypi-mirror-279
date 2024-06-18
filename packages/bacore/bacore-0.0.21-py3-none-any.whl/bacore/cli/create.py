"""Create CLI module."""
import subprocess as sup
from bacore.domain import settings
from bacore.domain.errors import PydValErrInfo
from bacore.interfaces import cli_typer
from pydantic import ValidationError
from rich import print
from typer import Argument, Exit, Typer, prompt
from typing import Annotated

app = Typer(rich_markup_mode="rich")


@app.command(rich_help_panel="Create")
def project(name: Annotated[str, Argument(help="Name of project ([red]no spaces allowed[/]).")] = ''):
    """Create new project ([blue]with hatch[/])."""
    cli_typer.verify_programs_installed(['hatch'])

    if name == '':
        name = prompt("Enter project name")

    try:
        new_project = settings.Project(name=name)
    except ValidationError as e:
        print(f'[red]{PydValErrInfo.error_msg(e)}[/red] Input was: "{PydValErrInfo.input(e)}"')
        raise Exit()

    print(f'Creating new project "{new_project.name}"[white]...[/]')
    sup.run(f'hatch new {new_project.name}', shell=True)
