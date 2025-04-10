"""Useful short functions for all kinds of usecases"""

import json
import re
from collections.abc import Iterable
from pathlib import Path
from unicodedata import normalize

import pandas as pd
from pandas import DataFrame, Series

from OSN_common.logger import logger


def categorize_age(age: int | None) -> str:
    """Categorize age into age groups"""
    if pd.isna(age):
        return pd.NA

    if age >= 19:
        return "dospeli"
    if age >= 16:
        return "deti_16"
    if age >= 7:
        return "deti_7"
    if age >= 1:
        return "deti_1"
    if age >= 0:
        return "deti_0"

    raise ValueError(f"Unrecognized age value: {age}")


def check_path_existence(paths: Iterable[Path]) -> None:
    """Existence test of path collection"""
    for p in paths:
        if not p.exists():
            logger.warning(f"Path does not exist! {p}")
            return
    logger.debug("✅ All paths exist")


def drop_duplicates(df: DataFrame, keep: str = "last") -> DataFrame:
    """Dropping duplicated rows from dataframe - keeping last occurence only.
    Warning: Fails if df contains lists or other unhashable types
    """
    if (n_dups := df.duplicated().sum()) > 0:
        logger.debug(f"Dropping {n_dups} duplicated rows")
        return df.drop_duplicates(keep=keep)

    logger.debug("✅ No duplicates found!")
    return df


def fillna_empty_list(s: Series) -> Series:
    """Fills NA values in a Series full of lists with empty lists"""
    return s.fillna("").apply(list)


def load_json(file: Path) -> list | dict:
    """Load JSON from file"""
    logger.debug(f"Loading JSON file: {file}")
    with file.open() as f:
        return json.load(f)


def move_column(df: DataFrame, colname: str, new_idx: int) -> DataFrame:
    """Move column 'colname' to a new position 'new_idx' in DataFrame 'df'"""
    col = df.pop(colname)
    df.insert(new_idx, colname, col)
    return df


def norm_path(p: Path) -> Path:
    """Normalize path so that e.g. accentation is consistent between multiple OS (e.g. 'š' between MacOS and Windows)"""
    return Path(normalize("NFC", str(p)))


def save_csv(df: DataFrame, csv_path: Path) -> None:
    """Save table 'df' as CSV file"""
    logger.info(f"Saving {len(df)} rows as CSV: {csv_path}")
    df.to_csv(csv_path, index=False, sep=";")


def shorten_path(p: Path, from_dir: Path) -> str:
    """Shorten path for logging purposes"""
    if from_dir not in p:
        return str(p)

    return f".../{p.relative_to(from_dir.parent)}"


def standardize_text(text: str) -> str:
    """Standardize text by removing non-alphanumeric characters and converting to lowercase"""
    return re.sub("[^0-9a-zA-Z]", "", text).lower()


def strip_df(df: DataFrame) -> DataFrame:
    """Remove empty / white characters and keep null values"""
    cols_txt = df.select_dtypes("object").columns
    for col in cols_txt:
        df[col] = df[col].fillna("").astype(str).str.strip().replace("", pd.NA)
    return df
