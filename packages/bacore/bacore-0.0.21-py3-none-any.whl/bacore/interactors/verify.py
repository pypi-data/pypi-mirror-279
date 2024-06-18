"""Module for verification."""
from typing import Protocol


class Exists(Protocol):
    """Protocol for verification of existing."""

    def verify_exists(self) -> bool:
        """Verify if exists."""
        ...


def command_on_path(command: Exists) -> bool:
    """Check if CLI command is on path."""
    return command.verify_exists()
