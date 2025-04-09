"""Basic tools for manipulation with XLSX Prílohy files"""

from pathlib import Path
from typing import Any

import pandas as pd
from pandas import DataFrame
from xlsxwriter.workbook import Workbook

import OSN_common.constants as c
from OSN_common.helpers import standardize_text, strip_df
from OSN_common.logger import logger

PRILOHY = c.PrilohyXlsxMeta()
P_FMT = c.PrilohyXlsxFormats()


def filter_valid_kod_ms(df: DataFrame, col_kod_ms: str = "kod_ms") -> DataFrame:
    """Keep rows where MS follows pattern SXX-XX where XX belongs to interval (00-99)"""
    df[col_kod_ms] = df[col_kod_ms].astype(str).str.strip()
    mask = df[col_kod_ms].str.fullmatch("S[0-9]{2}-[0-9]{2}")
    return df[mask].reset_index(drop=True)


def filter_valid_diagnoses(df: DataFrame, col_kod_diag: str = "kod_diagnozy") -> DataFrame:
    """Keep rows where Diag code follows YX where Y is a single letter and X is from interval (00-9999)"""
    df[col_kod_diag] = df[col_kod_diag].astype(str).str.strip()
    mask = df[col_kod_diag].str.fullmatch("^[A-Za-z][0-9]{2,4}")
    return df[mask].reset_index(drop=True)


def load_priloha_1(xlsx_path: str | Path) -> DataFrame:
    """Load data from XLSX file of Príloha 1"""
    df = pd.read_excel(xlsx_path, usecols="A:J", names=PRILOHY.P1["columns"])

    # remove header, footer
    cols_notna = ["cislo_programu", "nazov_programu", "uroven_programu", "od"]
    df = df.dropna(subset=cols_notna, how="any")

    mask = df[cols_notna].notna().all(axis=1)
    df = df[mask].reset_index(drop=True)

    df["cislo_programu"] = df["cislo_programu"].astype(int)

    for col in ["od", "do"]:
        df[col] = pd.to_datetime(df[col], format="%d.%m.%Y")

    # convert 'program II. úrovne' -> 2
    df["uroven_programu"] = (
        df["uroven_programu"].apply(lambda x: x.split(" ")[1][:-1]).map(c.ROMAN_2_INT, na_action="ignore")
    )
    df = strip_df(df)

    logger.debug(f"Loaded rows of XLSX Príloha 1: {len(df)}")
    return df


def load_priloha_2(xlsx_path: str | Path) -> DataFrame:
    """Load data from XLSX file of Príloha 2"""
    df = pd.read_excel(xlsx_path, names=PRILOHY.P2["columns"])

    # remove header, footer and section names
    df = filter_valid_kod_ms(df)

    df.cislo_programu = df.cislo_programu.astype(int)
    df.zdielana_ms = df.zdielana_ms == "ZD"

    # make stripped
    for col in ["kod_ms", "nazov_ms", "sposob_urcenia"]:
        df[col] = df[col].fillna("").astype(str).str.strip()

    # make numerical
    for col in c.UROVNE_MS_COLS:
        df[col] = df[col].replace(c.ROMAN_2_INT).astype("Int64")

    df.casova_dostupnost = df.casova_dostupnost.astype("Int64")
    df.minimum_na_nemocnicu = df.minimum_na_nemocnicu.apply(lambda x: int(x) if pd.notna(x) and "*" not in x else x)
    df.minimum_na_lekara = df.minimum_na_lekara.astype("Int64")

    logger.debug(f"Loaded rows of XLSX Príloha 2: {len(df)}")
    return df


def load_priloha_3(xlsx_path: str | Path) -> DataFrame:  # noqa: D103
    raise NotImplementedError("Cannot load since Príloha 3 is a full-text DOCX document.")


def load_priloha_4(xlsx_path: str | Path) -> DataFrame:  # noqa: D103
    raise NotImplementedError("Cannot load since Príloha 4 is a full-text DOCX document.")


def load_priloha_5(xlsx_path: str | Path) -> tuple[DataFrame, DataFrame]:
    """Load data from XLSX file of Príloha 5"""
    df = pd.read_excel(xlsx_path, names=PRILOHY.P5["columns"])

    # MS part
    df_ms = filter_valid_kod_ms(df)
    df_ms = strip_df(df_ms)
    df_ms["drg"] = df_ms["drg"].replace('Akákoľvek skupina klasifikačného systému začínajúca na "P"', "P")

    # TODO: change from hard-coded to exact or move to constants
    df_crit = pd.DataFrame(
        data={
            "kod": ["8p107", "8p133", "8q902", "Z515", "8r2637", "93083", "mOSNnovo"],
            "typ_kodu": ["vykon", "vykon", "vykon", "diagnoza", "vykon", "vykon", "marker"],
            "nazov": [
                "Vysokofrekvenčná ventilácia",
                "Inhalačná aplikácia oxidu dusnatého",
                "Aktívne kontrolované chladenie po resuscitácii, terapeutická hypotermia",
                "Paliatívna starostlivosť",
                "Výmenná transfúzia u novorodencov",
                "Akútny pôrod novorodenca v prípade ohrozenia života",
                "Nemožnosť transportu novorodenca z medicínskych príčin na vyššie pracovisko",
            ],
            "kriterium": [
                "Nekonvenčná UPV (vysokofrekvenčná, NO ventilácia)",
                "Nekonvenčná UPV (vysokofrekvenčná, NO ventilácia)",
                "Riadená hypotermia",
                "Paliatívna starostlivosť u novorodencov",
                "Potreba výmennej transfúzie",
                "Akútny pôrod novorodenca v prípade ohrozenia života bez ohľadu na gestačný vek a hmotnosť",
                "Marker - nemožnosť transportu novorodenca z medicínskych príčin na vyššie pracovisko",
            ],
        },
    )

    logger.debug(f"Loaded rows of XLSX Príloha 5 (MS + criteria): {len(df_ms)} + {len(df_crit)}")
    return df_ms, df_crit


def load_priloha_6(xlsx_path: str | Path) -> tuple[DataFrame, DataFrame]:
    """Load data from XLSX file of Príloha 6"""
    df = pd.read_excel(xlsx_path, names=PRILOHY.P6["columns"])

    # remove header, footer and section names
    df = filter_valid_kod_ms(df)
    df = strip_df(df)

    df["drg"] = df["drg"].replace("Skupina klasifikačného systému začínajúca na „W“", "W")
    df_dospeli = df.head(len(df) // 2).reset_index(drop=True)
    df_deti = df.tail(len(df) // 2).reset_index(drop=True)

    logger.debug(f"Loaded rows of XLSX Príloha 6 (dospeli + deti): {len(df_dospeli)} + {len(df_deti)}")
    return df_dospeli, df_deti


def load_priloha_7(xlsx_path: str | Path) -> tuple[DataFrame, DataFrame]:
    """Load data from XLSX file of Príloha 7"""
    df = pd.read_excel(xlsx_path, names=PRILOHY.P7["columns"])

    # remove header, footer and section names
    df = filter_valid_kod_ms(df)
    df = strip_df(df)

    df_hv = (
        df[df.nazov_ms.notna()]
        .reset_index(drop=True)
        .rename(columns={"kod_vykonu": "kod_hlavneho_vykonu", "nazov_vykonu": "nazov_hlavneho_vykonu"})
    )

    df_vv = df[df.nazov_ms.isna()].reset_index(drop=True)
    df_vv["nazov_ms"] = df_hv["nazov_ms"].values[0]

    logger.debug(f"Loaded rows of XLSX Príloha 7 (HV + VV) deti: {len(df_hv)} + {len(df_vv)}")
    return df_hv, df_vv


def load_priloha_7a(xlsx_path: str | Path) -> tuple[DataFrame, DataFrame]:
    """Load data from XLSX file of Príloha 7a"""
    df = pd.read_excel(xlsx_path, names=PRILOHY.P7a["columns"])

    # remove header, footer and section names
    df = filter_valid_kod_ms(df)
    df = strip_df(df)

    markers = df[df.kod_vykonu.str.startswith("m")].copy().drop("nazov_ms", axis=1).reset_index(drop=True)
    markers.columns = ["kod_markera", "nazov_markera", "kod_ms"]

    df = df[~df.kod_vykonu.str.startswith("m")]

    logger.debug(f"Loaded rows of XLSX Príloha 7a (markery + vykony) deti: {len(markers)} + {len(df)}")
    return df, markers


def load_priloha_8(xlsx_path: str | Path) -> tuple[DataFrame, DataFrame]:
    """Load data from XLSX file of Príloha 8"""
    df = pd.read_excel(xlsx_path, names=PRILOHY.P8["columns"])

    # remove header, footer and section names
    df = filter_valid_kod_ms(df)
    df = strip_df(df)

    df_hv = (
        df[df.nazov_ms.notna()]
        .reset_index(drop=True)
        .rename(columns={"kod_vykonu": "kod_hlavneho_vykonu", "nazov_vykonu": "nazov_hlavneho_vykonu"})
    )
    df_vv = df[df.nazov_ms.isna()].reset_index(drop=True)
    df_vv["nazov_ms"] = df_hv["nazov_ms"].values[0]

    logger.debug(f"Loaded rows of XLSX Príloha 8 (HV + VV) dospeli: {len(df_hv)} + {len(df_vv)}")
    return df_hv, df_vv


def load_priloha_8a(xlsx_path: str | Path) -> tuple[DataFrame, DataFrame]:
    """Load data from XLSX file of Príloha 8a"""
    df = pd.read_excel(xlsx_path, names=PRILOHY.P8a["columns"])

    # remove header, footer and section names
    df = filter_valid_kod_ms(df)
    df = strip_df(df)

    markers = df[df.kod_vykonu.str.startswith("m")].copy().drop("nazov_ms", axis=1).reset_index(drop=True)
    markers.columns = ["kod_markera", "nazov_markera", "kod_ms"]

    df = df[~df.kod_vykonu.str.startswith("m")]

    logger.debug(f"Loaded rows of XLSX Príloha 8a (markery + vykony) dospeli: {len(markers)} + {len(df)}")
    return df, markers


def load_priloha_9(xlsx_path: str | Path) -> tuple[DataFrame, DataFrame, DataFrame]:
    """Load data from XLSX file of Príloha 9
    Warning: Relies on the order of rows in the XLSX file.
    """
    df = pd.read_excel(xlsx_path, names=PRILOHY.P9["columns"], dtype=str)
    df = df[df["kod_ms"].notna()].reset_index(drop=True)

    # MS part
    df_ms = filter_valid_kod_ms(df)
    # TODO: make this more robust (don't rely on the order of rows)
    first_ms_dospeli = "S02-04"
    first_ms_idx = df_ms["kod_ms"][df_ms["kod_ms"] == first_ms_dospeli].index[0]
    df_deti = df_ms.iloc[:first_ms_idx]
    df_dospeli = df_ms.iloc[first_ms_idx:]

    # Diags part
    # TODO: make this more robust (don't rely on the order of rows)
    first_diag = "c910-"
    first_diag_idx = df["kod_ms"][df["kod_ms"] == first_diag].index[0]
    df_diags = df.iloc[first_diag_idx:].reset_index(drop=True)
    df_diags = df_diags.drop(["kod_hlavneho_vykonu", "nazov_hlavneho_vykonu"], axis=1)
    df_diags = df_diags.rename(
        columns={"drg": "skupina_diagnoz", "kod_ms": "kod_hlavnej_diagnozy", "nazov_ms": "nazov_hlavnej_diagnozy"},
    )
    logger.debug(
        f"Loaded rows of Príloha 9 (HV dospeli + HV deti + VD): {len(df_dospeli)} + {len(df_deti)} + {len(df_diags)}",
    )

    return df_dospeli, df_deti, df_diags


def load_priloha_9a(xlsx_path: str | Path) -> DataFrame:
    """Load data from XLSX file of Príloha 9a
    Warning: Relies on the order of rows in the XLSX file.
    """
    df = pd.read_excel(xlsx_path, names=PRILOHY.P9a["columns"], dtype=str)
    df_markera = filter_valid_kod_ms(df, col_kod_ms="kod_hlavnej_diagnozy")
    kod_markera, nazov_markera, _, kod_ms, nazov_ms = df_markera.loc[0].values

    # diagnozy
    df = df.dropna(subset="kod_hlavnej_diagnozy").reset_index(drop=True)
    # TODO: make this more robust (don't rely on the order of rows)
    first_diag = "f431"
    first_diag_idx = df["kod_hlavnej_diagnozy"][df["kod_hlavnej_diagnozy"] == first_diag].index[0]
    df = df.iloc[first_diag_idx:].reset_index(drop=True)

    df = df.drop(["kod_markera", "nazov_markera"], axis=1)
    df["kod_markera"] = kod_markera
    df["nazov_markera"] = nazov_markera
    df["kod_ms"] = kod_ms
    df["nazov_ms"] = nazov_ms

    logger.debug(f"Loaded rows of Príloha 9a (MD dospeli): {len(df)}")
    return df


def load_priloha_10(xlsx_path: str | Path) -> tuple[DataFrame, DataFrame, DataFrame]:
    """Load data from XLSX file of Príloha 10"""
    df = pd.read_excel(xlsx_path, names=PRILOHY.P10["columns"], dtype=str)
    df = df.dropna(subset="kod_hlavnej_diagnozy")
    df = strip_df(df)
    df = filter_valid_diagnoses(df, "kod_hlavnej_diagnozy")

    # vedlajsia diagnoza
    df_vd = filter_valid_kod_ms(df)
    diags_vd = set(df_vd["kod_hlavnej_diagnozy"])
    df_dospeli = df_vd.head(1)
    df_deti = df_vd.loc[1:]

    # hlavna diagnoza
    df_hd = df[~df["kod_hlavnej_diagnozy"].isin(diags_vd)].reset_index(drop=True)
    df_hd["kod_hlavnej_diagnozy"] = df_hd["kod_hlavnej_diagnozy"].apply(standardize_text)
    df_hd = df_hd.drop(columns=["kod_ms", "nazov_ms"])

    msg_counts = f"{len(df_dospeli)} + {len(df_deti)} + {len(df_hd)}"
    logger.debug(f"Loaded rows of XLSX Príloha 10 (VD dospeli + VD deti + HD): {msg_counts}")
    return df_dospeli, df_deti, df_hd


def load_priloha_11(xlsx_path: str | Path) -> None:  # noqa: D103
    raise NotImplementedError("Cannot load since Príloha 11 does not exist")


def load_priloha_12(xlsx_path: str | Path) -> DataFrame:
    """Load data from XLSX file of Príloha 12"""
    df = pd.read_excel(xlsx_path, names=PRILOHY.P12["columns"], dtype=str)
    df = filter_valid_kod_ms(df)
    df = strip_df(df)

    logger.debug(f"Loaded rows of XLSX Príloha 12 (vykony): {len(df)}")
    return df


def load_priloha_13(xlsx_path: str | Path) -> DataFrame:
    """Load data from XLSX file of Príloha 13"""
    df = pd.read_excel(xlsx_path, names=PRILOHY.P13["columns"], dtype=str)
    df = filter_valid_kod_ms(df)
    df = strip_df(df)

    logger.debug(f"Loaded rows of XLSX Príloha 13 (vykony): {len(df)}")
    return df


def load_priloha_14(xlsx_path: str | Path) -> DataFrame:
    """Load data from XLSX file of Príloha 14"""
    df = pd.read_excel(xlsx_path, names=PRILOHY.P14["columns"], dtype=str)
    df = filter_valid_kod_ms(df)
    df = strip_df(df)
    df.kod_diagnozy = df.kod_diagnozy.apply(standardize_text)

    logger.debug(f"Loaded rows of XLSX Príloha 14 (diagnozy): {len(df)}")
    return df


def load_priloha_15(xlsx_path: str | Path) -> DataFrame:
    """Load data from XLSX file of Príloha 15"""
    df = pd.read_excel(xlsx_path, names=PRILOHY.P15["columns"], dtype=str)
    df = filter_valid_kod_ms(df)
    df = strip_df(df)
    df.kod_diagnozy = df.kod_diagnozy.apply(standardize_text)

    logger.debug(f"Loaded rows of XLSX Príloha 15 (diagnozy): {len(df)}")
    return df


def load_priloha_16(xlsx_path: str | Path) -> DataFrame:
    """Load data from XLSX file of Príloha 16"""
    df = pd.read_excel(xlsx_path, names=PRILOHY.P16["columns"], dtype=str)
    df = df.dropna(subset="kod_diagnozy")
    df = filter_valid_diagnoses(df, "kod_diagnozy")
    df = strip_df(df)

    df["kod_diagnozy"] = df["kod_diagnozy"].apply(standardize_text)
    logger.debug(f"Loaded rows of XLSX Príloha 16 (diagnozy): {len(df)}")
    return df


def load_priloha_17(xlsx_path: str | Path) -> DataFrame:
    """Load data from XLSX file of Príloha 17"""
    df = pd.read_excel(xlsx_path, names=PRILOHY.P17["columns"], dtype=str)
    df = filter_valid_kod_ms(df)
    df = strip_df(df)

    logger.debug(f"Loaded rows of XLSX Príloha 17 (markery): {len(df)}")
    return df


def sort_priloha_2(df: DataFrame) -> DataFrame:
    """Sorting logic for P2"""
    columns_order = [
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
    ascending_order = [True, False, False, False, False, False, False, True, False]

    df["max_uroven"] = df[c.UROVNE_MS_COLS].max(axis=1)
    df = df.sort_values(columns_order, ascending=ascending_order).reset_index(drop=True)
    return df.drop("max_uroven", axis=1)


def sort_priloha_12_13(df: DataFrame, ordered_programs: list[int], p2: DataFrame) -> DataFrame:
    """Sorting logic for P12 & P13"""
    # preprocess p2
    cols = ["kod_ms", "cislo_programu", *c.UROVNE_MS_COLS]

    p2 = p2[~p2.zdielana_ms & p2.cislo_programu.isin(ordered_programs)][cols]
    p2["max_uroven"] = p2[c.UROVNE_MS_COLS].max(axis=1)
    p2 = p2.reset_index(names="ms_order")
    p2 = p2.drop(columns=c.UROVNE_MS_COLS)

    # merge to p12 / p13
    df = df.merge(p2, on="kod_ms")
    df["cislo_programu"] = pd.Categorical(df["cislo_programu"], categories=ordered_programs, ordered=True)
    df = df.sort_values(
        ["max_uroven", "cislo_programu", "ms_order", df.columns[0]],
        ascending=[False, True, True, True],
    )
    return df.drop(columns=["max_uroven", "cislo_programu", "ms_order"])


def set_formats(wb: Workbook) -> dict[str, Any]:
    """Decorate workbook 'wb' with useful formats"""
    return {
        "bigger_bold": wb.add_format(P_FMT.BIGGER_BOLD_FONT),
        "bold": wb.add_format(P_FMT.BOLD_FONT),
        "data_header": wb.add_format(
            {
                **P_FMT.BOLD_FONT,
                **P_FMT.CENTER_ALIGN,
                **P_FMT.TEXT_WRAP,
                **P_FMT.GREY_BG,
            },
        ),
        "data_header_bottom": wb.add_format(
            {
                **P_FMT.BOLD_FONT,
                **P_FMT.CENTER_ALIGN,
                **P_FMT.TEXT_WRAP,
                **P_FMT.GREY_BG,
                **P_FMT.THICK_BOTTOM_BORDER,
            },
        ),
        "data_header_rotated": wb.add_format(
            {
                **P_FMT.BOLD_FONT,
                **P_FMT.TEXT_WRAP,
                **P_FMT.GREY_BG,
                **P_FMT.THICK_BOTTOM_BORDER,
                **P_FMT.RIGHT_ROTATION,
                **P_FMT.CENTER_ALIGN,
            },
        ),
        "data_row": wb.add_format({**P_FMT.TEXT_WRAP, **P_FMT.DEFAULT_FONT, **P_FMT.THIN_BOTTOM_BORDER}),
        "data_row_bold": wb.add_format(
            {
                **P_FMT.BOLD_FONT,
                **P_FMT.CENTER_ALIGN,
                **P_FMT.TEXT_WRAP,
                **P_FMT.THIN_BOTTOM_BORDER,
            },
        ),
        "data_row_center": wb.add_format(
            {
                **P_FMT.TEXT_WRAP,
                **P_FMT.DEFAULT_FONT,
                **P_FMT.CENTER_ALIGN,
                **P_FMT.THIN_BOTTOM_BORDER,
            },
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
            },
        ),
        "superscript": wb.add_format({**P_FMT.DEFAULT_FONT, **P_FMT.SUPERSCRIPT}),
        "uroven_I": wb.add_format({**P_FMT.UROVEN_I_BG}),
        "uroven_II": wb.add_format({**P_FMT.UROVEN_II_BG}),
        "uroven_III": wb.add_format({**P_FMT.UROVEN_III_BG}),
        "uroven_IV": wb.add_format({**P_FMT.UROVEN_IV_BG}),
        "uroven_V": wb.add_format({**P_FMT.UROVEN_V_BG}),
    }
