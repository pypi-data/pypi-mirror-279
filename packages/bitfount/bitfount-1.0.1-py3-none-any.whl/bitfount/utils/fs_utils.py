"""Utility functions to interact with the filesystem."""

from pathlib import Path
from typing import Callable

MAX_FILE_NUM = 100


def safe_append_to_file(func: Callable[[Path], None], initial_path: Path) -> None:
    """Handle PermissionError when writing to a file.

    Execute some function that writes to a file and if it's not possible
    to write due to a PermissionError (e.g. the user has opened the file
    in Windows so can't be appended to) try to write to a new file instead.

    Args:
        func: Function to execute, that takes in the destination file path.
        initial_path: The desired destination file path.
    """
    try:
        func(initial_path)
    except PermissionError as error:
        if initial_path.exists():
            i = 1
            new_path = (
                initial_path.parent / f"{initial_path.stem}{i}{initial_path.suffix}"
            )
            while new_path.exists() and i < MAX_FILE_NUM:
                i += 1
                new_path = (
                    initial_path.parent / f"{initial_path.stem}{i}{initial_path.suffix}"
                )
            if new_path.exists():
                raise error
            func(new_path)
        else:
            raise error
