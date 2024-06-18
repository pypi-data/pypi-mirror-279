"""Serve CLI module."""
import subprocess as sup
from bacore.domain import settings
from bacore.domain.errors import PydValErrInfo
from bacore.interfaces import cli_typer
from pydantic import ValidationError
from rich import print
from typer import Argument, Exit, Option, Typer, prompt
from typing import Annotated

app = Typer(rich_markup_mode="rich")


@app.command(rich_help_panel="Serve")
def documentation(project: Annotated[str, Argument(help="Name of project.")] = '',
                  port: Annotated[int, Option(help="Port to serve documentation on.")] = 8000):
    """Serve documentation with MkDocs for a project."""
    cli_typer.verify_programs_installed(['mkdocs'])

    if project == '':
        project = prompt("Enter project name")

    try:
        project = settings.Project(name=project)
    except ValidationError as e:
        print(f'[red]{PydValErrInfo.error_msg(e)}[/red] Input was: "{PydValErrInfo.input(e)}"')
        raise Exit()

    print(f'Serving documentation for project "{project.name}"[white]...[/]')
    sup.run(f"mkdocs serve -a 127.0.0.1:{port} &", shell=True)
