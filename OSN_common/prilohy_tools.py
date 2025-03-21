import pandas as pd
from pandas import DataFrame
from pathlib import Path
from xlsxwriter.workbook import Workbook

import OSN_common.constants as c
from OSN_common.helpers import standardize_text, strip_df
from OSN_common.logger import logger

PRILOHY = c.PrilohyXlsxMeta()
P_FMT = c.PrilohyXlsxFormats()


def load_priloha_1(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(xlsx_path, skiprows=6, skipfooter=6, usecols="A:J", names=PRILOHY.P1["columns"])

    for col in c.P1_DATE_COLS:
        df[col] = pd.to_datetime(df[col], format="%d.%m.%Y")

    # convert 'program II. úrovne' -> 2
    df["uroven_programu"] = (
        df["uroven_programu"].apply(lambda x: x.split(" ")[1][:-1]).map(c.ROMAN_2_INT, na_action="ignore")
    )
    df = strip_df(df)

    logger.debug(f"Loaded rows of XLSX Príloha 1: {len(df)}")
    return df


def load_priloha_2(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(xlsx_path, skiprows=8, skipfooter=101, names=PRILOHY.P2["columns"])

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
        df[col] = pd.to_numeric(df[col], errors="ignore")

    # enforce stripped strings
    for col in ["kod_ms", "nazov_ms", "sposob_urcenia"]:
        df[col] = df[col].str.strip()

    logger.debug(f"Loaded rows of XLSX Príloha 2: {len(df)}")
    return df


def load_priloha_3(xlsx_path: str) -> DataFrame:
    raise NotImplementedError()


def load_priloha_4(xlsx_path: str) -> DataFrame:
    raise NotImplementedError()


def load_priloha_5(xlsx_path: str) -> DataFrame:
    raise NotImplementedError()


def load_priloha_6(xlsx_path: str) -> DataFrame:
    raise NotImplementedError()


def load_priloha_7(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(xlsx_path, skiprows=7, skipfooter=10, names=PRILOHY.P7["columns"], dtype=str)

    logger.debug(f"Loaded rows of Príloha 7: {len(df)}")
    return strip_df(df)


def load_priloha_8(xlsx_path: str) -> DataFrame:
    raise NotImplementedError()


def load_priloha_9(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(
        xlsx_path,
        skiprows=9,
        skipfooter=14,
        names=PRILOHY.P9["columns"],
        dtype=str,
    )

    logger.debug(f"Loaded rows of Príloha 9: {len(df)}")
    return strip_df(df)


def load_priloha_10(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(
        xlsx_path,
        skiprows=7,
        skipfooter=7,
        names=PRILOHY.P10["columns"],
        dtype=str,
    )
    df = strip_df(df)
    df.kod_hlavnej_diagnozy = df.kod_hlavnej_diagnozy.fillna("").apply(standardize_text)

    logger.debug(f"Loaded rows of XLSX Príloha 10: {len(df)}")
    return df


def load_priloha_11(xlsx_path: str) -> DataFrame:
    raise NotImplementedError("Príloha 11 doesn't exist")


def load_priloha_12(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(
        xlsx_path,
        skiprows=7,
        skipfooter=26,
        names=PRILOHY.P12["columns"],
        dtype=str,
    )
    df = strip_df(df)
    df = df.dropna(how="all")

    logger.debug(f"Loaded rows of XLSX Príloha 12: {len(df)}")
    return df


def load_priloha_13(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(
        xlsx_path,
        skiprows=7,
        skipfooter=26,
        names=PRILOHY.P13["columns"],
        dtype=str,
    )
    df = strip_df(df)
    df = df.dropna(how="all")

    logger.debug(f"Loaded rows of XLSX Príloha 13: {len(df)}")
    return df


def load_priloha_14(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(
        xlsx_path,
        skiprows=7,
        skipfooter=9,
        names=PRILOHY.P14["columns"],
        dtype=str,
    )
    df = strip_df(df)
    df = df.dropna(how="all")
    df.kod_diagnozy = df.kod_diagnozy.fillna("").apply(standardize_text)

    logger.debug(f"Loaded rows of XLSX Príloha 14: {len(df)}")
    return df


def load_priloha_15(xlsx_path: str) -> DataFrame:
    df = pd.read_excel(
        xlsx_path,
        skiprows=7,
        skipfooter=9,
        names=PRILOHY.P15["columns"],
        dtype=str,
    )
    df = strip_df(df)
    df = df.dropna(how="all")
    df.kod_diagnozy = df.kod_diagnozy.fillna("").apply(standardize_text)

    logger.debug(f"Loaded rows of XLSX Príloha 15: {len(df)}")
    return df


def save_priloha(df: DataFrame, csv_path: Path, **kwargs) -> None:
    logger.info(f"Saving {len(df)} rows as a CSV table: .../{csv_path.relative_to(csv_path.parent.parent.parent)}")
    strip_df(df).to_csv(csv_path, index=False, sep=";")


def sort_priloha_2(df: DataFrame) -> DataFrame:
    """
    Sorting logic for P2
    """
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
    df = df.drop("max_uroven", axis=1)
    return df


def sort_priloha_12_13(df: DataFrame, ordered_programs: list[int], p2: DataFrame) -> DataFrame:
    """
    Sorting logic for P12 & P13
    """

    # preprocess p2
    cols = ["kod_ms", "cislo_programu"] + c.P2_UROVNE_COLS

    p2 = p2[~p2.zdielana_ms & p2.cislo_programu.isin(ordered_programs)][cols]
    p2["max_uroven"] = p2[c.P2_UROVNE_COLS].max(axis=1)
    p2 = p2.reset_index(names="ms_order")
    p2 = p2.drop(columns=c.P2_UROVNE_COLS)

    # merge to p12 / p13
    df = df.merge(p2, on="kod_ms")
    df["cislo_programu"] = pd.Categorical(df["cislo_programu"], categories=ordered_programs, ordered=True)
    df = df.sort_values(
        ["max_uroven", "cislo_programu", "ms_order", df.columns[0]],
        ascending=[False, True, True, True],
    )
    df = df.drop(columns=["max_uroven", "cislo_programu", "ms_order"])
    return df


def set_formats(wb: Workbook) -> dict:
    return {
        "bigger_bold": wb.add_format(P_FMT.BIGGER_BOLD_FONT),
        "bold": wb.add_format(P_FMT.BOLD_FONT),
        "data_header": wb.add_format(
            {
                **P_FMT.BOLD_FONT,
                **P_FMT.CENTER_ALIGN,
                **P_FMT.TEXT_WRAP,
                **P_FMT.GREY_BG,
            }
        ),
        "data_header_bottom": wb.add_format(
            {
                **P_FMT.BOLD_FONT,
                **P_FMT.CENTER_ALIGN,
                **P_FMT.TEXT_WRAP,
                **P_FMT.GREY_BG,
                **P_FMT.THICK_BOTTOM_BORDER,
            }
        ),
        "data_header_rotated": wb.add_format(
            {
                **P_FMT.BOLD_FONT,
                **P_FMT.TEXT_WRAP,
                **P_FMT.GREY_BG,
                **P_FMT.THICK_BOTTOM_BORDER,
                **P_FMT.RIGHT_ROTATION,
                **P_FMT.CENTER_ALIGN,
            }
        ),
        "data_row": wb.add_format({**P_FMT.TEXT_WRAP, **P_FMT.DEFAULT_FONT, **P_FMT.THIN_BOTTOM_BORDER}),
        "data_row_bold": wb.add_format(
            {
                **P_FMT.BOLD_FONT,
                **P_FMT.CENTER_ALIGN,
                **P_FMT.TEXT_WRAP,
                **P_FMT.THIN_BOTTOM_BORDER,
            }
        ),
        "data_row_center": wb.add_format(
            {
                **P_FMT.TEXT_WRAP,
                **P_FMT.DEFAULT_FONT,
                **P_FMT.CENTER_ALIGN,
                **P_FMT.THIN_BOTTOM_BORDER,
            }
        ),
        "default": wb.add_format({**P_FMT.TEXT_WRAP, **P_FMT.DEFAULT_FONT}),
        "diff_added": wb.add_format({**P_FMT.LIGHT_GREEN_BG}),
        "diff_edited": wb.add_format({**P_FMT.LIGHT_YELLOW_BG}),
        "diff_original": wb.add_format({**P_FMT.LIGHT_ORANGE_BG, **P_FMT.STRIKEOUT}),
        "diff_removed": wb.add_format({**P_FMT.LIGHT_RED_BG, **P_FMT.STRIKEOUT}),
        "diff_same": wb.add_format(),
        "italic": wb.add_format({**P_FMT.ITALIC_FONT, **P_FMT.TEXT_WRAP}),
        "priloha_header": wb.add_format({**P_FMT.BOLD_FONT, **P_FMT.RIGHT_ALIGN}),
        "program_header": wb.add_format(
            {
                **P_FMT.BOLD_FONT,
                **P_FMT.TEXT_WRAP,
                **P_FMT.LIGHT_BLUE_BG,
                **P_FMT.THIN_BOTTOM_BORDER,
            }
        ),
        "superscript": wb.add_format({**P_FMT.DEFAULT_FONT, **P_FMT.SUPERSCRIPT}),
        "uroven_I": wb.add_format({**P_FMT.UROVEN_I_BG}),
        "uroven_II": wb.add_format({**P_FMT.UROVEN_II_BG}),
        "uroven_III": wb.add_format({**P_FMT.UROVEN_III_BG}),
        "uroven_IV": wb.add_format({**P_FMT.UROVEN_IV_BG}),
        "uroven_V": wb.add_format({**P_FMT.UROVEN_V_BG}),
    }
