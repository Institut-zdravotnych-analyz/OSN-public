import json
import pandas as pd
from pandas import DataFrame, Series
from pathlib import Path
import re
from typing import Any, Iterable
from unicodedata import normalize

from OSN_common.logger import logger


def categorize_age(age: Any) -> str:
    """
    Categorize age into age groups
    """
    if pd.isna(age):
        return pd.NA

    if age >= 19:
        return "dospeli"
    elif age >= 16:
        return "deti_16"
    elif age >= 7:
        return "deti_7"
    elif age >= 1:
        return "deti_1"
    elif age >= 0:
        return "deti_0"
    else:
        logger.warning(f"Unrecognized age value: {age}")
        return ""


def check_path_existence(paths: Iterable[Path]) -> None:
    """
    Bulk existence test of path collection
    """
    for p in paths:
        if not p.exists():
            logger.warning(f"Path does not exist! {p}")
            return
    logger.info("✅ All paths exist")


def drop_duplicates(df: DataFrame, keep="last") -> DataFrame:
    """
    Informative duplicates dropping - keeping last occurence
    Warning: Fails if df contains lists or other unhashable types
    """
    if (n_dups := df.duplicated().sum()) > 0:
        logger.debug(f"Dropping {n_dups} duplicated rows")
        return df.drop_duplicates(keep=keep)

    logger.debug("✅ No duplicates found!")
    return df


def fillna_empty_list(s: Series):
    """
    Fills NA values in a Series full of lists with empty lists
    """
    return s.fillna("").apply(list)


def load_json(file: str | Path) -> list | dict:
    with open(file, "r") as f:
        return json.load(f)


def move_column(df: DataFrame, colname: str, new_idx: int) -> DataFrame:
    """
    Move column 'colname' to a new position 'new_idx' in DataFrame 'df'
    """
    col = df.pop(colname)
    df.insert(new_idx, colname, col)
    return df


def norm_path(p: Path) -> Path:
    """
    Normalize path so that e.g. accentation is consistent between multiple OS (e.g. 'š' between MacOS and Windows)
    """
    return Path(normalize("NFC", str(p)))


def standardize_text(text: str) -> str:
    """
    Standardize text by removing non-alphanumeric characters and converting to lowercase
    """
    return re.sub("[^0-9a-zA-Z]", "", text).lower()


def strip_df(df: DataFrame) -> DataFrame:
    """
    Remove empty characters and keep null values
    """
    cols_txt = df.select_dtypes("object").columns
    df[cols_txt] = df[cols_txt].apply(lambda x: x.str.strip())
    return df
