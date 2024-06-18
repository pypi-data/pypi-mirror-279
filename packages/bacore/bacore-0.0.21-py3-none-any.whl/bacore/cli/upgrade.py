"""CLI upgrade commands."""
import subprocess as sup
from typer import Argument, Typer
from typing_extensions import Annotated

app = Typer(rich_markup_mode="rich")
state = {"verbose": False}


@app.command(rich_help_panel="Upgrade")
def homebrew():
    """Upgrade Homebrew and all packages installed with it."""
    sup.run("brew update && brew upgrade && brew cleanup && brew doctor", shell=True)


@app.command(rich_help_panel="Upgrade")
def emacs(uninstall: Annotated[int, Argument(help="Emacs version to uninstall.")] = 29,
          install: Annotated[int, Argument(help="Emacs version to install.")] = 29):
    """Emacs"""
    sup.run(f"brew uninstall emacs-plus@{uninstall}", shell=True)
    sup.run(f"brew install emacs-plus@{install} \
    --with-dbus \
    --with-mailutils \
    --with-no-frame-refocus \
    --with-imagemagic \
    --with-native-comp", shell=True)
