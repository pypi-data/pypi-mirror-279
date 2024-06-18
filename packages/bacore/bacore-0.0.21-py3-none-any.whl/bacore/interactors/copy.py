"""Module for copy interactors."""
import subprocess as sup
from pathlib import Path
from typing import Optional


def rsync_copy(source: Path, destination: Path, file_filter: Optional[str]):
    """Use rsync to mirror files and folders from src to dest."""
    try:
        sup.run(f"rsync -av --delete {source}/{file_filter} {destination}", shell=True)
    except FileNotFoundError:
        print(f"Unable to find source: [pink]{source}[/pink]")
