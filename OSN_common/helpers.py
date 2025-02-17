import pandas as pd
from pandas import NA, DataFrame, Series
from pathlib import Path
import os
import re
from typing import Any
from unicodedata import normalize


def categorize_age(age: Any) -> str:
    """
    Categorize age into age groups
    """
    if pd.isna(age):
        return NA
    
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
        print(f"Unrecognized age value: {age}")
        return 


def drop_duplicates(df: DataFrame, keep='last') -> DataFrame:
    """
    Informative duplicates dropping - keeping last occurence
    Warning: Fails if df contains lists or other unhashable types
    """
    if (n_dups := df.duplicated().sum()) > 0:
        print(f"Dropping {n_dups} duplicated rows")
        return df.drop_duplicates(keep=keep)
    print("No duplicates found")
    return df

def fillna_empty_list(s: Series):
    """
    Fills NA values in a Series full of lists with empty lists
    """
    return s.fillna('').apply(list)

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
    Normalize path so that e.g. accentation is consistent between OS (e.g. "š" between MacOS and Windows)
    """
    return Path(normalize('NFC', str(p)))

def rimska_cislica(cislo):
    rimske_cislice = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
    return rimske_cislice[cislo]

def standardize_text(text: str) -> str:
    """
    Standardize text by removing non-alphanumeric characters and converting to lowercase
    """
    return re.sub("[^0-9a-zA-Z]", "", text).lower()

def strip_df(df: DataFrame) -> DataFrame:
    """
    Remove empty characters and keep null values
    """
    cols_txt = df.select_dtypes('object').columns
    df[cols_txt] = df[cols_txt].apply(lambda x: x.str.strip())
    return df


# TODO move to constants
OSN_PATH = os.environ.get("OSN_data")
if OSN_PATH is None:
    raise ValueError("Environmental variable 'OSN_data' is not set. In order to continue please run 'export OSN_data=<path_to_data>'")
else:
    OSN_PATH = Path(OSN_PATH).expanduser()
    DATA_PATH = norm_path(OSN_PATH / '11_Dátové súbory a prevodníky')
    if not DATA_PATH.exists():
        raise ValueError("Environmental variable 'OSN_data' is wrong. In order to continue please run 'export OSN_data=<path_to_data>'")

ROMAN_2_INT = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5}
INT_2_ROMAN = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V'}
UROVNE_COLS = [
    'uroven_ms_dospeli', 
    'uroven_ms_deti_0', 
    'uroven_ms_deti_1', 
    'uroven_ms_deti_7', 
    'uroven_ms_deti_16'
]