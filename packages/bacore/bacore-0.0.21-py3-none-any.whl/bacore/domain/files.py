"""Module domain files for handling of files and directories."""
import tomllib
from pathlib import Path


class TOML:
    """TOML file class."""

    def __init__(self, path: Path):
        """Initialize."""
        self.path = path

    @property
    def path(self):
        """Get file path."""
        return self._path

    @path.setter
    def path(self, value):
        """Set file path as pathlib.Path object."""
        if not isinstance(value, Path):
            raise TypeError("Path must be a pathlib.Path object.")
        self._path = value

    def data_to_dict(self) -> dict:
        """Content as dictionary."""
        with open(self.path, mode="rb") as f:
            content = tomllib.load(f)
        return content
