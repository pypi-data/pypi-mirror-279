from __future__ import annotations

import logging

log = logging.getLogger("red_utils.ext.dataframe_utils.pandas_utils")

from pathlib import Path
from typing import Union

from red_utils.ext.dataframe_utils.validators.pandas_validators import (
    VALID_COL_TYPES,
    validate_df_col_type,
)

from .constants import PANDAS_DATE_FORMAT, PANDAS_DATETIME_FORMAT, PANDAS_TIME_FORMAT

import pandas as pd

def get_oldest_newest(
    df: pd.DataFrame = None, date_col: str = None, filter_cols: list[str] | None = None
) -> Union[pd.Series, pd.DataFrame]:
    """Get the oldest and newest rows in a DataFrame.

    Params:
        df (pd.DataFrame): Pandas DataFrame to work on
        date_col (str): Name of the column to sort by
        filter_cols (list[str]): List of column names to return with the oldest/newest record.

    Returns:
        (pandas.Series|pandas.DataFrame): A Pandas `DataFrame` or `Series` containing oldest & newest records
        in the input `DataFrame`.

    """
    if df is None or df.empty:
        raise ValueError("Missing or empty DataFrame")
    if date_col is None:
        raise ValueError("Missing name of date column to sort by")

    try:
        min_date = df[date_col].min()
        oldest = df.loc[df[date_col] == min_date]

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception getting min date value from column [{date_col}]. Details: {exc}"
        )
        log.error(msg)

        raise exc

    try:
        max_date = df[date_col].max()
        newest = df.loc[df[date_col] == max_date]

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception getting max date value from column [{date_col}]. Details: {exc}"
        )
        log.error(msg)

        raise exc

    if filter_cols is not None:
        try:
            oldest = oldest[filter_cols]
            newest = newest[filter_cols]
        except Exception as exc:
            msg = Exception(f"Unhandled exception filtering columns. Details: {exc}")
            log.error(msg)

            raise exc

    return oldest, newest


def rename_df_cols(
    df: pd.DataFrame = None, col_rename_map: dict[str, str] = None
) -> pd.DataFrame:
    """Return a DataFrame with columns renamed based on input col_rename_map.

    Params:
        df (pandas.DataFrame): A Pandas `DataFrame` with columns to rename
            col_rename_map (dict[str, str]): A Python `dict` defining existing column names and the value
            they should be renamed to.

    Returns:
        (pandas.DataFrame): A renamed Pandas `DataFrame`.

    """
    if col_rename_map is None:
        msg = ValueError("No col_rename_map passed")
        log.warning(msg)

        return df

    if df is None or df.empty:
        msg = ValueError("Missing DataFrame, or DataFrame is empty")
        log.error(msg)

        raise ValueError(msg)

    try:
        df = df.rename(columns=col_rename_map)

        return df
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception renaming DataFrame columns. Details: {exc}"
        )
        log.error(msg)

        raise exc


def count_df_rows(df: pd.DataFrame = None) -> int:
    """Return count of the number of rows in a DataFrame.

    Params:
        df (pandas.DataFrame): A Pandas `DataFrame` to count the rows in

    Returns:
        (int): Count of rows in a `DataFrame`

    """
    if df is not None:
        if df.empty:
            return
    else:
        return

    if not isinstance(df, pd.DataFrame) and not isinstance(df, pd.Series):
        raise TypeError(
            f"Invalid type for DataFrame: ({type(df)}). Must be a Pandas Series or DataFrame"
        )

    return len(df.index)


def load_pqs_to_df(
    search_dir: str = None, filetype: str = ".parquet"
) -> list[pd.DataFrame]:
    """Load data export files in search_dir into list of DataFrames.

    Params:
        search_dir (str): The directory to search for files in
        filetype (str): The file extension to filter results by

    Returns:
        (list[pandas.DataFrame]): A list of Pandas `DataFrame`s created from files in `search_dir`

    """
    if search_dir is None:
        raise ValueError("Missing a directory to search")

    if not filetype.startswith("."):
        filetype = f".{filetype}"

    files: list[Path] = []

    for f in Path(search_dir).glob(f"**/*{filetype}"):
        if f.is_file():
            files.append(f)

    dataframes: list[pd.DataFrame] = []

    if filetype == ".parquet":
        for pq in files:
            df = load_pq(pq_file=pq)

            dataframes.append(df)

    elif filetype == ".csv":
        for f in files:
            df = pd.read_csv(f)

            dataframes.append(df)

    return dataframes


def convert_csv_to_pq(
    csv_file: Union[str, Path] = None,
    pq_file: Union[str, Path] = None,
    dedupe: bool = False,
) -> bool:
    """Read a CSV file into a DataFrame, then write the DataFrame to a Parquet file.

    Params:
        csv_file (str|Path): Path to a CSV file to read from
        pq_file (str|Path): Path to a Parquet file to write to
        dedupe (bool): Whether to run .drop_duplicates() on the DataFrame

    Returns:
        (bool): `True` if `csv_file` is converted to `pq_file` successfully

    Raises:
        Exception: If file cannot be saved, an `Exception` is raised instead of returning
            a bool value

    """
    if csv_file is None:
        raise ValueError("Missing a CSV input file to read from")
    if pq_file is None:
        raise ValueError("Missing a Parquet file to save to")

    if isinstance(csv_file, str):
        csv_file: Path = Path(csv_file)
    if isinstance(pq_file, str):
        pq_file: Path = Path(pq_file)

    if not csv_file.exists():
        raise FileNotFoundError(f"Could not find input CSV file at path: {csv_file}")

    try:
        df = load_csv(csv_file=csv_file)
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception reading CSV file '{csv_file}' to DataFrame. Details: {exc}"
        )
        log.error(msg)

        raise exc

    try:
        success = save_pq(df=df, pq_file=pq_file, dedupe=dedupe)

        return success

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception writing DataFrame to file: {pq_file}. Details: {exc}"
        )
        log.error(msg)

        raise exc


def convert_pq_to_csv(
    pq_file: Union[str, Path] = None,
    csv_file: Union[str, Path] = None,
    dedupe: bool = False,
) -> bool:
    """Read a Parquet file into a DataFrame, then write the DataFrame to a CSV file.

    Params:
        pq_file (str|Path): Path to a Parquet file to read from
        csv_file (str|Path): Path to a CSV file to write to
        dedupe (bool): Whether to run .drop_duplicates() on the DataFrame

    Returns:
        (bool): `True` if `pq_file` is converted to `csv_file` successfully

    Raises:
        Exception: If file cannot be saved, an `Exception` is raised instead of returning
            a bool value

    """
    if csv_file is None:
        raise ValueError("Missing a CSV file to save to")
    if pq_file is None:
        raise ValueError("Missing an input Parquet file to read from")

    if isinstance(csv_file, str):
        csv_file: Path = Path(csv_file)
    if isinstance(pq_file, str):
        pq_file: Path = Path(pq_file)

    if not pq_file.exists():
        raise FileNotFoundError(f"Could not find input Parquet file at path: {pq_file}")

    try:
        df = load_pq(pq_file=pq_file)
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception reading Parquet file '{pq_file}' to DataFrame. Details: {exc}"
        )
        log.error(msg)

        raise exc

    try:
        success = save_csv(df=df, csv_file=csv_file, columns=df.columns, dedupe=dedupe)

        return success

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception writing DataFrame to file: {csv_file}. Details: {exc}"
        )
        log.error(msg)

        raise exc


def load_pq(
    pq_file: Union[str, Path] = None, pq_engine: str = "pyarrow"
) -> pd.DataFrame:
    """Return a DataFrame from a previously saved .parquet file.

    Params:
        pq_file (str|Path): Path to a `.parquet` file to load

    Returns:
        (pandas.DataFrame): A Pandas `DataFrame` loaded from a `.parquet` file

    """
    if pq_file is None:
        raise ValueError("Missing pq_file to load")
    if isinstance(pq_file, str):
        pq_file: Path = Path(pq_file)

    if not pq_file.suffix == ".parquet":
        pq_file: Path = Path(f"{pq_file}.parquet")

    if not pq_file.exists():
        msg = FileNotFoundError(f"Could not find Parquet file at '{pq_file}'")
        # log.error(msg)
        log.error(msg)

        raise exc

    try:
        df = pd.read_parquet(pq_file, engine=pq_engine)

        return df

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception loading Parquet file '{pq_file}' to DataFrame. Details: {exc}"
        )
        log.error(msg)

        raise exc


def save_pq(
    df: pd.DataFrame = None,
    pq_file: Union[str, Path] = None,
    dedupe: bool = False,
    pq_engine: str = "pyarrow",
) -> bool:
    """Save DataFrame to a .parquet file.

    Params:
        df (pandas.DataFrame): A Pandas `DataFrame` to save
        pq_file (str|Path): The path to a `.parquet` file where the `DataFrame` should be saved
        dedupe (bool): If `True`, deduplicate the `DataFrame` before saving

    Returns:
        (bool): `True` if `DataFrame` is saved to `pq_file` successfully
        (bool): `False` if `DataFrame` is not saved to `pq_file` successfully

    Raises:
        Exception: If file cannot be saved, an `Exception` is raised

    """
    if df is None or df.empty:
        msg = ValueError("DataFrame is None or empty")
        log.warning(msg)

        return False

    if pq_file is None:
        raise ValueError("Missing output path")
    if isinstance(pq_file, str):
        pq_file: Path = Path(pq_file)

    if pq_file.suffix != ".parquet":
        new_str = str(f"{pq_file}.parquet")
        pq_file: Path = Path(new_str)

    if not pq_file.parent.exists():
        try:
            pq_file.parent.mkdir(exist_ok=True, parents=True)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception creating directory: {pq_file.parent}. Details: {exc}"
            )
            log.error(msg)

            return False

    try:
        if dedupe:
            df = df.drop_duplicates()

        output = df.to_parquet(path=pq_file, engine=pq_engine)

        return True

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception saving DataFrame to Parquet file: {pq_file}. Details: {exc}"
        )
        log.error(msg)
        raise exc


def load_csv(csv_file: Union[str, Path] = None, delimiter: str = ",") -> pd.DataFrame:
    """Load a CSV file into a DataFrame.

    Params:
        csv_file (str|Path): The path to a `.csv` file to load into a `DataFrame
        delimiter (str): The delimiter symbol the `csv_file` uses

    Returns:
        (pandas.DataFrame): A Pandas `DataFrame` with data loaded from the `csv_file`

    """
    if csv_file is None:
        raise ValueError("Missing output path")

    if isinstance(csv_file, str):
        csv_file: Path = Path(csv_file)

    if csv_file.suffix != ".csv":
        new_str = str(f"{csv_file}.csv")
        csv_file: Path = Path(new_str)

    if not csv_file.exists():
        msg = FileNotFoundError(f"Could not find CSV file: '{csv_file}'.")
        log.error(msg)
        raise exc

    try:
        df = pd.read_csv(csv_file, delimiter=delimiter)

        return df

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception loading DataFrame from CSV file: {csv_file}. Details: {exc}"
        )
        log.error(msg)

        raise exc


def save_csv(
    df: pd.DataFrame = None,
    csv_file: Union[str, Path] = None,
    columns: list[str] = None,
    dedupe: bool = False,
) -> bool:
    """Save DataFrame to a .csv file.

    Params:
        df (pandas.DataFrame): A Pandas `DataFrame` to save
        csv_file (str|Path): The path to a `.csv` file where the `DataFrame` should be saved
        columns (list[str]): A list of string values representing column names for the `.csv` file
        dedupe (bool): If `True`, deduplicate the `DataFrame` before saving

    Returns:
        (bool): `True` if `DataFrame` is saved to `csv_file` successfully
        (bool): `False` if `DataFrame` is not saved to `csv_file` successfully

    Raises:
        Exception: If file cannot be saved, an `Exception` is raised

    """
    if df is None or df.empty:
        msg = ValueError("DataFrame is None or empty")

        return False

    if csv_file is None:
        raise ValueError("Missing output path")
    if isinstance(csv_file, str):
        csv_file: Path = Path(csv_file)

    if csv_file.suffix != ".csv":
        new_str = str(f"{csv_file}.csv")
        csv_file: Path = Path(new_str)

    if not csv_file.parent.exists():
        try:
            csv_file.parent.mkdir(exist_ok=True, parents=True)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception creating directory: {csv_file.parent}. Details: {exc}"
            )
            log.error(msg)

            return False

    if columns is None:
        columns = df.columns

    try:
        if dedupe:
            df = df.drop_duplicates()

        if columns is not None:
            output = df.to_csv(csv_file, columns=columns)
        else:
            output = df.to_csv(csv_file)

        return True

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception saving DataFrame to Parquet file: {csv_file}. Details: {exc}"
        )
        log.error(msg)
        raise exc
