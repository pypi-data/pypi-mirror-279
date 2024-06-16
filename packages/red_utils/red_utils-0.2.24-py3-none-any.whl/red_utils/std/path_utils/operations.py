from __future__ import annotations

import logging

log = logging.getLogger("red_utils.std.path_utils")

from datetime import datetime
import json
import os
from pathlib import Path
import shutil
from typing import Any, Union

from red_utils.core.constants import JSON_DIR

from .constants import VALID_RETURN_TYPES

def file_ts(fmt: str = "%Y-%m-%d_%H:%M:%S") -> str:
    """Return a formatted timestamp, useful for prepending to dir/file names.

    Params:
        fmt (str): String that defines the format of a timestamp

    Returns:
        (str): A formatted datetime string

    """
    now: str = datetime.now().strftime(fmt)

    return now


def export_json(
    input: Union[str, list[list, dict], dict[str, Any]] = None,
    output_dir: str = JSON_DIR,
    output_filename: str = f"{file_ts()}_unnamed_json.json",
):
    """Export JSON object to an output file.

    Params:
        input (str|list[list,dict]|dict[str,Any]): The input object to be output to a file.
        output_dir (str): The directory where a .json file will be saved.
        output_filename (str): The name of the file that will be saved in output_dir.

    Raises:
        FileExistsError: When the output path already exists
        FileNotFoundError: When the export path does not exist
        Exception: When other exceptions have not been caught, a generic `Exception` is raised

    """
    if not Path(output_dir).exists():
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    if isinstance(input, dict):
        input = json.dumps(input)

    if Path(f"{output_dir}/{output_filename}").exists():
        raise FileExistsError(
            f"JSON file already exists: {output_dir}/{output_filename}"
        )

    if output_dir.endswith("/"):
        output_dir = output_dir[:-1]

    if not output_filename.endswith(".json"):
        output_filename = f"{output_filename}.json"

    output_path: str = f"{output_dir}/{output_filename}"

    log.debug(f"Output path: {output_path}")

    if not Path(output_path).exists():
        try:
            with open(output_path, "w+") as f:
                f.write(input)
        except FileExistsError as file_exists_exc:
            log.error(file_exists_exc)

            raise file_exists_exc
        except FileNotFoundError as file_not_found_exc:
            log.error(file_not_found_exc)
            raise file_not_found_exc
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception writing JSON to file: {output_path}. Details: {exc}"
            )
            log.error(msg)

            raise exc


def extract_file_ext(path: Path = None) -> str:
    """Extract full file extension from a Path.

    Description:
        Given a file with multiple file extensions, i.e. `file.tar.gz`,
        this function will join all suffixes (`.tar`, `.gz`) into a single string.
        A `Path.suffix` on its own only returns the last suffix (i.e. `.gz`).

    Params:
        path (Path): A `pathlib.Path` object to a file. Path is checked with `.is_file()`, skipping directories passed by mistake.

    """
    assert path, ValueError("Missing a file path")
    assert isinstance(path, Path), TypeError(
        f"path must be a pathlib.Path object. Got type: ({type(path)})"
    )
    if not path.is_file():
        log.error(
            ValueError(f"[WARNING] path should be a file, but {path} is a directory.")
        )

        return ""

    ## Extract all suffixes from file path
    suffixes: list[str] = path.suffixes

    if len(suffixes) > 1:
        ## Join suffixes, i.e. [".tar", ".gz"] -> ".tar.gz"
        return "".join(suffixes)

    elif len(suffixes) == 1:
        ## Return [".suffix"] -> ".suffix"
        return suffixes[0]

    else:
        ## No suffix(es) detected, return empty string

        return ""


def scan_dir(
    target: Union[str, Path] = None,
    as_str: bool = False,
    as_pathlib: bool = False,
    return_type: str = "all",
) -> Union[list[os.DirEntry, str, Path]]:
    """Return a list of path strings found in self.path.

    Params:
        as_str (bool): If `True`, returns a list of paths formatted as Python strings.
        as_pathlib (bool): If `True`, returns a list of paths formatted as Python `pathlib.Path` objects.
        return_type (str): Control return type.
            Options:
                - `all`: Return both files & dirs
                - `files`: Return only files
                - `dirs`: Return only dirs

    Returns:
        list[os.DirEntry]: (default) If `as_str = False`
        list[str]: If `as_str = True`
        list[pathlib.Path]: If `as_str = False` and `as_pathlib = True`.

    """
    ## Validate return_type
    if not return_type:
        log.warning("return_type cannot be None. Defaulting to 'all'.")
        return_type = "all"
    else:
        return_type: str = return_type.lower()
        assert isinstance(return_type, str), TypeError(
            f"return_type must be of type str. Got type: {type(return_type)}"
        )
        assert return_type in VALID_RETURN_TYPES, ValueError(
            f"Invalid return type: '{return_type}'. Must be one of {VALID_RETURN_TYPES}"
        )

    ## Validate as_str/as_pathlib
    if as_str and as_pathlib:
        log.warning(
            "as_str and as_pathlib cannot both be true. Defaulting to as_str=True, as_pathlib=False"
        )
        as_pathlib = False

    ## Validate target
    assert target is not None, ValueError("target cannot be None")
    assert isinstance(target, str) or isinstance(target, Path), TypeError(
        f"target must be of type str or pathlib.Path. Got type: {type(target)}"
    )
    target: Path = Path(f"{target}")
    if "~" in f"{target}":
        target: Path = target.expanduser()

    assert target.exists(), FileNotFoundError(
        f"Could not find target path: '{target}'."
    )

    ## Initialize empty list to store found paths
    paths: list[os.DirEntry] = []

    ## Scan target directory
    for p in os.scandir(target):
        if return_type == "all":
            ## Append path
            paths.append(p)
        elif return_type == "files":
            if Path(p.path).is_file():
                ## Append file path
                paths.append(p)
        elif return_type == "dirs":
            if Path(p.path).is_dir():
                ## Append dir path
                paths.append(p)

    if as_str:
        ## Convert all found paths to str type
        _paths: list[str] = []

        for p in paths:
            _path: str = p.path

            _paths.append(_path)

        return _paths

    elif as_pathlib:
        ## Convert all found paths to pathlib.Path type
        _paths: list[Path] = []

        for p in paths:
            _path: Path = Path(p.path)
            _paths.append(_path)

        return _paths

    else:
        ## Return list of os.DirEntry types
        return paths


def crawl_dir(
    target: Union[str, Path] = None,
    filetype_filter: str | None = None,
    return_type: str = "all",
) -> Union[dict[str, list[Path]]]:
    """Crawl a directory and return an object with all found files & dirs.

    Params:
        target (str | Path): The target directory to crawl
        filetype_filter (str): An optional filetype filter str; only files matching this filter will be returned
        return_type (str): Return `files`, `dirs`, or `all`

    Returns:
        (list[Path]): A list of `Path` objects if `return_type` is `dirs` or `files`
        (dict[str, list[Path]]): If `return_type` is `all`, return a dict `{"file": [], "dirs": []}`

    Raises:
        ValueError: When input validation fails
        FileNotFoundError: When a file/directory path cannot be found

    """

    def validate_target(target: Union[str, Path] = target) -> Path:
        """Validate a target path.

        Params:
            target (str, Path): The path to validate

        Returns:
            (Path): A Python `Path` object

        Raises:
            ValueError: When input validation fails
            FileNotFoundError: When the path to validate does not exist

        """
        if target is None:
            raise ValueError("Missing a target directory to scan")
        target: Path = Path(f"{target}")
        if "~" in f"{target}":
            target: Path = target.expanduser()
        if not target.exists():
            exc = FileNotFoundError(f"Could not find directory: {target}")
            log.error(exc)

            raise exc

        return target

    def validate_return_type(
        return_type: str = return_type,
        VALID_RETURN_TYPES: list[str] = VALID_RETURN_TYPES,
    ) -> str:
        """Validate a return type.

        Params:
            return_type (str): The `return_type` string to validate
            VALID_RETURN_TYPES `list[str]`: Valid options for the `return_type` string. Defaults to a predefined list of `["all", "files", "dirs"]`

        Returns:
            (str): The validated `return_type` string

        Raises:
            ValueError: When input validation fails
            TypeError: When input value is not a `str`

        """
        if return_type is None:
            raise ValueError("Missing return type")
        if not isinstance(return_type, str):
            raise TypeError(
                f"Invalid type for return_type: ({type(return_type)}). Must be one of {VALID_RETURN_TYPES}"
            )
        if return_type not in VALID_RETURN_TYPES:
            exc = ValueError(
                f"Invalid return type: {return_type}. Must be one of: {VALID_RETURN_TYPES}"
            )
            log.error(exc)

            raise exc

        return return_type

    def _crawl(
        target=target, search_str: str = "**/*", return_type=return_type
    ) -> Union[dict[str, list[Path]], list[Path]]:
        """Run Path crawl.

        Inherits `target`, `search_str`, and `return_type` from parent method that calls this function.
        """
        return_obj: dict[str, list[Path]] = {"files": [], "dirs": []}

        log.info(f"Crawling target: {target} ...")

        for i in target.glob(search_str):
            if i.is_file():
                if return_type in ["all", "files"]:
                    return_obj["files"].append(i)
                else:
                    pass
            else:
                if return_type in ["all", "dirs"]:
                    return_obj["dirs"].append(i)

        match return_type:
            case "all":
                return return_obj
            case "files":
                return return_obj["files"]
            case "dirs":
                return return_obj["dirs"]

    if filetype_filter:
        if not isinstance(filetype_filter, str):
            raise TypeError(
                f"Invalid type for filetype_filter: ({type(filetype_filter)}). Must be of type str"
            )
        if not filetype_filter.startswith("."):
            filetype_filter: str = f".{filetype_filter}"

        search_str: str = f"**/*{filetype_filter}"
    else:
        search_str: str = "**/*"

    target: Path = validate_target()
    return_type: str = validate_return_type()

    return_obj = _crawl(target=target, search_str=search_str, return_type=return_type)

    return return_obj


def list_files(
    in_dir: str = None, ext_filter: str = None, return_files: list[Path] = []
) -> list[Path]:
    """List all files in a path, optionally filtering by file extension.

    Params:
        in_dir (str): Directory path to scan
        ext_filter (str): Filetype to search for
        return_files (list[Path]): Used by the function to recurse through subdirectories

    Returns:
        (list[Path]): A list of found files, represented as `Path` objects

    """
    if not in_dir:
        raise ValueError("Missing input directory to search")
    if ext_filter is not None:
        if not ext_filter.startswith("."):
            ext_filter = f".{ext_filter}"

    if ext_filter:
        search_str: str = f"**/*{ext_filter}"
    else:
        search_str: str = "**/*"

    return_files: list[Path] = []

    try:
        for _p in Path(in_dir).glob(search_str):
            if _p.is_file():
                return_files.append(_p)
            elif _p.is_dir():
                list_files(in_dir=_p, ext_filter=ext_filter, return_files=return_files)

        return return_files

    except FileNotFoundError as fnf:
        msg = Exception(f"Could not find input path: {in_dir}. Details: {fnf}")
        log.error(msg)

        raise fnf
    except PermissionError as perm:
        msg = Exception(f"Could not open path: {in_dir}. Details: {perm}")
        log.error(msg)

        raise perm
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception looping input path: {in_dir}. Details: {exc}"
        )
        log.error(msg)

        raise exc


def ensure_dirs_exist(ensure_dirs: list[Union[str, Path]] = None) -> None:
    """Loop over a list of directories and create any paths that do not already exist.

    Params:
        ensure_dirs (list[str]|list[Path]): A list of directory paths formatted as strings or Path objects.
            If any list item is of type str, it will be converted to a Path.
    """
    if not ensure_dirs:
        raise ValueError("Missing list of directories to ensure existence")

    validated_list: list[Path] = []

    for i in ensure_dirs:
        if isinstance(i, str):
            i = Path(i)
            validated_list.append(i)
        elif isinstance(i, Path):
            validated_list.append(i)
        else:
            log.error(
                ValueError(
                    f"Invalid type for list item: ({type(i)}). Must be of type str or Path."
                )
            )
            pass

    ensure_dirs = validated_list

    for d in ensure_dirs:
        if not d.exists():
            try:
                d.mkdir(exist_ok=True, parents=True)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception creating directory: {d}. Details: {exc}"
                )
                log.error(msg)
                pass


def delete_path(rm_path: Union[str, Path] = None) -> bool:
    """Recursively delete a path.

    Params:
        rm_path (str | Path): The path to delete

    Returns:
        (bool): `True` if `rm_path` deleted successfully
        (bool): `False` if `rm_path` not deleted successfully

    Raises:
        FileNotFoundError: When path to delete does not exist
        PermissionError: When permission to delete the path is not granted
        Exception: Generic `Exception` when operation fails and is not caught by another exception

    """
    if rm_path is None:
        raise ValueError("Missing a path to remove.")
    if isinstance(rm_path, str):
        rm_path: Path = Path(rm_path)

    try:
        if rm_path.is_file():
            rm_path.unlink()
        elif rm_path.is_dir():
            shutil.rmtree(rm_path)

        return True

    except FileNotFoundError as fnf:
        msg = Exception(f"Could not find file {str(rm_path)}. Details: {fnf}")
        log.error(msg)

        return False
    except PermissionError as perm:
        msg = Exception(
            f"Insufficient permissions to delete file {str(rm_path)}. Details: {perm}"
        )
        log.error(msg)

        return False
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception deleting file {str(rm_path)}. Details: {exc}"
        )
        log.error(msg)

        return False
