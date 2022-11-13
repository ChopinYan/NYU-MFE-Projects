import os
import pathlib

import torch


def to_list(tensor):
    return tensor.detach().cpu().tolist()


def to_tensor(vector):
    tensor = torch.tensor(vector, dtype=torch.float)
    return tensor


def create_path(pathname: str) -> None:
    """Creates the directory for the given path if it doesn't already exist."""
    directory = str(pathlib.Path(pathname).parent)
    if not os.path.exists(directory):
        os.makedirs(directory)


def filename(*paths) -> str:
    """Given a path relative to this project's top-level directory, returns the
    full path in the OS.
    Args:
        paths: A list of folders/files.  These will be joined in order with "/"
            or "\" depending on platform.
    Returns:
        The full absolute path in the OS.
    """
    # First parent gets the scripts directory, and the second gets the top-level.
    result_path = pathlib.Path(__file__).resolve().parent.parent
    for path in paths:
        result_path /= path
    return str(result_path)

