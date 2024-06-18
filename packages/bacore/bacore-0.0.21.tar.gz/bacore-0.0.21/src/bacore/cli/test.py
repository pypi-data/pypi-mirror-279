"""Test CLI module."""
import subprocess as sup
from bacore import config
from bacore.interfaces import cli_typer
from typer import Option, Typer
from typing import Annotated

app = Typer(rich_markup_mode="rich")


@app.command(rich_help_panel="Test")
def dev(in_container: Annotated[bool, Option("--in-container", "-c", help="Run tests in Docker container.")] = False,
        memray: Annotated[bool, Option("--memcheck", "-m", help="Inspect memory usage while running tests.")] = False):
    """Run all tests continuously [red](includes doctests)[/]"""
    monitor_memory = "--memray" if memray else ""
    if in_container:
        if config.docker_build is not None:
            sup.run(f"ptw -cw src tests -- {monitor_memory} --doctest-modules -s", shell=True)
        sup.run(f"docker-compose run -it --rm --entrypoint ptw dev -cw src tests -- {monitor_memory} --doctest-modules -s", shell=True)
    else:
        sup.run(f"ptw -cw src tests -- {monitor_memory} --doctest-modules -s", shell=True)
