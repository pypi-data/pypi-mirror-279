"""Delete interactors."""
from datetime import datetime, timedelta
from pathlib import Path
from pydantic import Field, validate_call
from pydantic.dataclasses import dataclass
from typing_extensions import Annotated


@dataclass
class DeletedFiles:
    """Deleted files summary."""

    path: Path
    pattern: str
    older_than_days: int
    recursive: bool
    number_of_deleted_files: int
    deleted_files: list[str]


@validate_call
def files(path: Path, pattern: str = "*", older_than_days: Annotated[int, Field(ge=0)] = 0,
          recursive: bool = False) -> DeletedFiles:
    """Delete files older than x days.

    Args:
      path (`Path`): Path to search for files.
      pattern (`str`): Pattern to search for files.
      older_than_days (`int`): Delete files older than x dyas. Default is `0`. Negative values are not allowed.
      recursive (`bool`): Optionally delete files recursively. Default is `False`.
    """
    number_of_deleted_files = 0
    deleted_files = []

    now = datetime.now()

    find_function = path.rglob if recursive else path.glob
    for file in find_function(pattern):
        if file.is_file() and file.stat().st_mtime < (now - timedelta(days=older_than_days)).timestamp():
            file.unlink()
            deleted_files.append(str(file))
            number_of_deleted_files += 1

    return DeletedFiles(path=path,
                        pattern=pattern,
                        older_than_days=older_than_days,
                        recursive=recursive,
                        number_of_deleted_files=number_of_deleted_files,
                        deleted_files=deleted_files
                        )
