import pandas as pd
from pandas import DataFrame
from pathlib import Path
from xlsxwriter.workbook import Workbook

from OSN_common.helpers import standardize_text, strip_df
from OSN_common.logger import logger
import OSN_common.constants as c


def load_priloha_1(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(
        xlsx_path,
        skiprows=6,
        skipfooter=6,
        usecols="A:J",
        names=c.P1_XLSX['columns']
    )

    for col in c.P1_DATE_COLS:
        df[col] = pd.to_datetime(df[col], format='%d.%m.%Y')

    # convert 'program II. úrovne' -> 2
    df["uroven_programu"] = (
        df["uroven_programu"].apply(lambda x: x.split(" ")[1][:-1]).map(c.ROMAN_2_INT, na_action="ignore")
    )
    df = strip_df(df)

    logger.info(f"Loaded rows of XLSX Príloha 1: {len(df)}")
    return df


def load_priloha_2(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(
        xlsx_path,
        skiprows=8,
        skipfooter=102,
        names=c.P2_XLSX['columns']
    )

    # dropping 78x 'Číslo programu', 78x NaN
    df["is_numeric"] = df.cislo_programu.astype(str).str.isnumeric()
    df = df[df["is_numeric"]].drop(columns=["is_numeric"])

    # dropping XLSX headers
    df = df[df.nazov_ms.notna()]

    # zdielanie -> bool
    df.zdielana_ms = df.zdielana_ms == "ZD"

    # enforce numerical
    for col in c.P2_UROVNE_COLS:
        df[col] = df[col].map(c.ROMAN_2_INT, na_action="ignore").astype("Int64")
    for col in ["cislo_programu"] + c.P2_NUM_COLS:
        df[col] = pd.to_numeric(df[col], errors='ignore')

    # enforce stripped strings
    for col in ["kod_ms", "nazov_ms", "sposob_urcenia"]:
        df[col] = df[col].str.strip()

    logger.info(f"Loaded rows of XLSX Príloha 2: {len(df)}")
    return df

def sort_priloha_2(df: DataFrame) -> DataFrame:
    SORT_ORDER = [
            "cislo_programu",
            "max_uroven",
            "uroven_ms_deti_0",
            "uroven_ms_deti_1",
            "uroven_ms_deti_7",
            "uroven_ms_deti_16",
            "uroven_ms_dospeli",
            "zdielana_ms",
            "kod_ms",
        ]
    ASCENDING_ORDER = [True, False, False, False, False, False, False, True, False]

    df["max_uroven"] = df[c.P2_UROVNE_COLS].max(axis=1)
    df = df.sort_values(SORT_ORDER, ascending=ASCENDING_ORDER).reset_index(drop=True)
    df = df.drop('max_uroven', axis=1)
    return df


def load_priloha_3(xlsx_path: str) -> DataFrame:
    NotImplementedError()


def load_priloha_4(xlsx_path: str) -> DataFrame:
    NotImplementedError()


def load_priloha_5(xlsx_path: str) -> DataFrame:
    NotImplementedError()


def load_priloha_6(xlsx_path: str) -> DataFrame:
    NotImplementedError()


def load_priloha_7(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(
        xlsx_path, 
        skiprows=7, 
        skipfooter=10, 
        names=c.P7_XLSX['columns'], 
        dtype=str
    )

    logger.info(f"Loaded rows of Príloha 7: {len(df)}")
    return strip_df(df)


def load_priloha_8(xlsx_path: str) -> DataFrame:
    NotImplementedError()


def load_priloha_9(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(
        xlsx_path,
        skiprows=9,
        skipfooter=14,
        names=c.P9_XLSX['columns'], 
        dtype=str,
    )

    logger.info(f"Loaded rows of Príloha 9: {len(df)}")
    return strip_df(df)


def load_priloha_10(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(
        xlsx_path,
        skiprows=7,
        skipfooter=7,
        names=c.P10_XLSX['columns'], 
        dtype=str,
    )
    df = strip_df(df)
    df.kod_hlavnej_diagnozy = df.kod_hlavnej_diagnozy.fillna("").apply(standardize_text)

    logger.info(f"Loaded rows of XLSX Príloha 10: {len(df)}")
    return df


def load_priloha_11(xlsx_path: str) -> DataFrame:
    NotImplementedError("Príloha 11 doesn't exist")


def load_priloha_12(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(
        xlsx_path,
        skiprows=7,
        skipfooter=26,
        names=c.P12_XLSX['columns'],
        dtype=str,
    )
    df = strip_df(df)
    df = df.dropna(how='all')

    logger.info(f"Loaded rows of XLSX Príloha 12: {len(df)}")
    return df


def load_priloha_13(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(
        xlsx_path,
        skiprows=7,
        skipfooter=23,
        names=c.P13_XLSX['columns'],
        dtype=str,
    )
    df = strip_df(df)
    df = df.dropna(how='all')

    logger.info(f"Loaded rows of XLSX Príloha 13: {len(df)}")
    return df


def load_priloha_14(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(
        xlsx_path,
        skiprows=7,
        skipfooter=9,
        names=c.P14_XLSX['columns'],
        dtype=str,
    )
    df = strip_df(df)
    df = df.dropna(how='all')
    df.kod_diagnozy = df.kod_diagnozy.fillna("").apply(standardize_text)

    logger.info(f"Loaded rows of XLSX Príloha 14: {len(df)}")
    return df


def load_priloha_15(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(
        xlsx_path,
        skiprows=7,
        skipfooter=3,
        names=c.P15_XLSX['columns'],
        dtype=str,
    )
    df = strip_df(df)
    df = df.dropna(how='all')
    df.kod_diagnozy = df.kod_diagnozy.fillna("").apply(standardize_text)

    logger.info(f"Loaded rows of XLSX Príloha 15: {len(df)}")
    return df


def postprocess_priloha(df: DataFrame, sortby: str = None) -> DataFrame:
    """
    Postprocess dataframe before dumping
    """
    # cislo programu -> int
    if "cislo_programu" in df.columns:
        df.cislo_programu = df.cislo_programu.astype(int)

    # MS names -> stripprf str, not finishing with '.' or ','
    if "nazov_ms" in df.columns:
        df["nazov_ms"] = (
            df["nazov_ms"]
            .fillna('')
            .str.strip()
            .apply(lambda x: x.replace("I.", "I") if x.endswith("I.") else x)
            .apply(lambda x: x[:-1] if x.endswith(",") else x)
        )

    # text columns - stripped
    for col in df.columns:
        if "nazov" in col or "kod" in col or "navrh" in col:
            df[col] = df[col].str.strip()

    # clean from duplicated
    df = df.drop_duplicates().reset_index(drop=True)

    # sort
    if sortby and sortby in df.columns:
        df = df.sort_values(sortby).reset_index(drop=True)

    return df


def save_priloha(df: DataFrame, csv_path: Path, **kwargs) -> None:
    logger.info(f"Saving {len(df)} rows as a CSV table: {csv_path.relative_to(csv_path.parent.parent)}")
    postprocess_priloha(df.copy(), **kwargs).to_csv(csv_path, index=False, sep=";")


def add_formats(wb: Workbook):
    # Define constants
    DEFAULT_FONT = {"font_name": "Times New Roman", "font_size": 12}
    BOLD_FONT = {"font_name": "Times New Roman", "font_size": 12, "bold": True}
    ITALIC_FONT = {"font_name": "Times New Roman", "font_size": 12, "italic": True}
    BIGGER_BOLD_FONT = {"font_name": "Times New Roman", "font_size": 14, "bold": True}
    RIGHT_ALIGN = {"align": "right"}
    CENTER_ALIGN = {"align": "center"}
    TEXT_WRAP = {"text_wrap": True}
    LIGHT_BLUE_BG = {"bg_color": "DDEBF7"}
    GREY_BG = {"bg_color": "D0CECE"}
    LIGHT_GREEN_BG = {"bg_color": "C4E59F"}
    LIGHT_RED_BG = {"bg_color": "FFBFBF"}
    LIGHT_YELLOW_BG = {"bg_color": "FFFBC2"}
    LIGHT_ORANGE_BG = {"bg_color": "FFE1C9"}
    BLUE_BG = {"bg_color": "CAD4E8"}
    UROVEN_I_BG = {"bg_color": "63be7b"}
    UROVEN_II_BG = {"bg_color": "b1d47f"}
    UROVEN_III_BG = {"bg_color": "ffeb84"}
    UROVEN_IV_BG = {"bg_color": "fcaa78"}
    UROVEN_V_BG = {"bg_color": "f8696b"}
    THIN_BOTTOM_BORDER = {"bottom": 1}
    THICK_BOTTOM_BORDER = {"bottom": 2}
    RIGHT_ROTATION = {"rotation": 90}
    SUPERSCRIPT = {"font_script": 1}
    STRIKEOUT = {"font_strikeout": True}

    return {
        "program_header": wb.add_format({**BOLD_FONT, **TEXT_WRAP, **LIGHT_BLUE_BG, **THIN_BOTTOM_BORDER}),
        "data_header": wb.add_format({**BOLD_FONT, **CENTER_ALIGN, **TEXT_WRAP, **GREY_BG}),
        "data_header_bottom": wb.add_format(
            {**BOLD_FONT, **CENTER_ALIGN, **TEXT_WRAP, **GREY_BG, **THICK_BOTTOM_BORDER}
        ),
        "data_header_rotated": wb.add_format(
            {
                **BOLD_FONT,
                **TEXT_WRAP,
                **GREY_BG,
                **THICK_BOTTOM_BORDER,
                **RIGHT_ROTATION,
                **CENTER_ALIGN,
            }
        ),
        "data_row": wb.add_format({**TEXT_WRAP, **DEFAULT_FONT, **THIN_BOTTOM_BORDER}),
        "data_row_bold": wb.add_format({**BOLD_FONT, **CENTER_ALIGN, **TEXT_WRAP, **THIN_BOTTOM_BORDER}),
        "data_row_center": wb.add_format({**TEXT_WRAP, **DEFAULT_FONT, **CENTER_ALIGN, **THIN_BOTTOM_BORDER}),
        "superscript": wb.add_format({**DEFAULT_FONT, **SUPERSCRIPT}),
        "uroven_I": wb.add_format({**UROVEN_I_BG}),
        "uroven_II": wb.add_format({**UROVEN_II_BG}),
        "uroven_III": wb.add_format({**UROVEN_III_BG}),
        "uroven_IV": wb.add_format({**UROVEN_IV_BG}),
        "uroven_V": wb.add_format({**UROVEN_V_BG}),
        "priloha_header": wb.add_format({**BOLD_FONT, **RIGHT_ALIGN}),
        "default": wb.add_format({**TEXT_WRAP, **DEFAULT_FONT}),
        "bold": wb.add_format(BOLD_FONT),
        "italic": wb.add_format({**ITALIC_FONT, **TEXT_WRAP}),
        "bigger_bold": wb.add_format(BIGGER_BOLD_FONT),
        "diff_added": wb.add_format({**LIGHT_GREEN_BG}),
        "diff_edited": wb.add_format({**LIGHT_YELLOW_BG}),
        "diff_removed": wb.add_format({**LIGHT_RED_BG, **STRIKEOUT}),
        "diff_same": wb.add_format(),
    }
