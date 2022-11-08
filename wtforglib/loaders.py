from os import PathLike
from pathlib import Path
from typing import Union

import yaml

from wtforglib.errors import raise_filenotfound


def load_yaml_file(filenm: Union[str, PathLike[str]], missing_ok: bool = True):
    """Loads a yaml file.

    Parameters
    ----------
    filenm : Union[str,PathLike[str]]
        The yaml file to load
    missing_ok : bool optional default True
        When False and file does not exist raises FileNotFound exeception

    Returns
    -------
    dict[Any, Any]
        Representing contents of filenm
    """
    ypath = Path(filenm)
    yaml_result = {}
    if ypath.exists() and ypath.is_file():
        with open(ypath, "r") as yfile:
            yaml_result = yaml.safe_load(yfile)
    elif not missing_ok:
        raise_filenotfound(ypath)
    return yaml_result
