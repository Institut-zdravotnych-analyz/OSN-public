from collections import defaultdict
import pandas as pd
from pandas import DataFrame
from pathlib import Path

from OSN_common.helpers import DATA_PATH, strip_df


_prevodove_subory = {
    "pzs_12": {
        "cesta": "03_Prevodníky/pzs_12_prevodnik.csv",
        "argumenty": {"sep": ";", "dtype": "str"},
    },
    "psc_na_zuj": {
        "cesta": "03_Prevodníky/psc_na_zuj.csv",
        "argumenty": {
            "sep": ";",
            "dtype": defaultdict(
                lambda: "str",
                {"ZUJ_pravdepodobnost": "float"},
            ),
        },
    },
}

def load_prevodovy_subor(nazov):
    if subor := _prevodove_subory.get(nazov):
        return pd.read_csv(DATA_PATH / subor["cesta"], **subor["argumenty"])
    else:
        raise ValueError(f"Prevodník s názvom {nazov} neexistuje.")

def load_programovy_profil(rok, verzia):
    return pd.read_csv(
        DATA_PATH
        / "03_Prevodníky"
        / "Vyhláška"
        / f"{verzia}"
        / f"programovy_profil_{verzia}_{rok}.csv",
        sep=";",
    )

def load_siet_nemocnic(rok):
    return pd.read_excel(
        DATA_PATH / "08_Nemocnice" / f"siet_nemocnic_{rok}.xlsx",
        index_col=[0, 1, 2, 3],
        header=[0, 1, 2],
    )

def load_signifikantne_operacne_vykony(rok):
    return pd.read_csv(
        DATA_PATH / "03_Prevodníky" / f"signifikantne_operacne_vykony_{rok}.csv",
        sep=";",
    )

def load_vtpn(rok):
    return pd.read_csv(DATA_PATH / "03_Prevodníky" / f"VTPN_{rok}.csv", sep=";")

def load_zoznam_diagnoz(csv_path: Path) -> DataFrame:
    df = pd.read_csv(
        csv_path,
        sep=";",
        converters={"zoznam_koncovych_diagnoz": eval},
    )
    cols_str = ['kod_diagnozy', 'nazov_diagnozy', 'kod_skupiny_diagnoz', 'uplny_kod_diagnozy', 'poznamka']
    df[cols_str] = df[cols_str].apply(lambda x: x.str.strip())

    print('Loaded (diagnozy):', len(df))
    return df


def load_zoznam_drg_skupin(csv_path: Path) -> DataFrame:
    df = pd.read_csv(
        csv_path,
        sep=";",
        skiprows=1,
        names=['drg', 'segment', 'popis', 'rel_vaha', 'treatment_time_mean']
    )
    df = strip_df(df)

    print('Loaded (DRG skupiny):', len(df))
    return df

def load_zoznam_ms(csv_path: Path) -> DataFrame:
    df = pd.read_csv(
        csv_path,
        sep=";",
        dtype=defaultdict(
            lambda: "str",
            zdielana_ms="boolean",
            uroven_ms_dospeli="Int8",
            uroven_ms_deti_0="Int8",
            uroven_ms_deti_1="Int8",
            uroven_ms_deti_7="Int8",
            uroven_ms_deti_16="Int8",
            cislo_programu="Int16",
        ),
    )
    cols_txt = ['kod_ms', 'nazov_ms', 'sposob_urcenia']
    df[cols_txt] = df[cols_txt].apply(lambda x: x.str.strip())

    print('Loaded (MS):', len(df))
    return df

def load_zoznam_nemocnic():
    return pd.read_csv(
        DATA_PATH / "08_Nemocnice" / f"zoznam_nemocnic.csv",
        sep=";",
        dtype=defaultdict(lambda: "str", uroven_nemocnice="Int8"),
    )

def load_zoznam_obci():
    return pd.read_excel(
        DATA_PATH / "03_Prevodníky" / "KÓDY_OBCE.xlsx",
        dtype=defaultdict(
            lambda: "str",
            {"Počet obyvateľov 2021": "Int64"},
        ),
    )

def load_zoznam_poistencov(rok):
    return pd.read_csv(
        DATA_PATH / "05_Poistenci" / f"poistenci_vyfiltrovani_{rok}.csv",
        sep=";",
        dtype=defaultdict(
            lambda: "str",
            kod_zp="Int8",
        ),
        parse_dates=["datum_narodenia"],
        date_format="ISO8601",
    )


def load_zoznam_vykonov(csv_path: Path) -> DataFrame:
    df = pd.read_csv(
        csv_path,
        sep=";",
        converters={"zoznam_terminalnych_vykonov": eval},
    )

    df = df.rename(columns={
        'Kapitola': 'kapitola',
        'Poznámka k vykazovaniu': 'poznamka_vykazovanie',
        'Signifikantný': 'significant',
        'POZNÁMKA': 'poznamka',
        'ZMENY OPROTI ZZV 2024': 'zmeny_zzv_2024'
    })

    # strip all text columns
    cols_txt = df.columns[2:-1]
    df[cols_txt] = df[cols_txt].apply(lambda x: x.str.strip())

    # keep "terminal" in case duplicates are found
    df = df[(~df['kod_vykonu'].duplicated(keep=False)) | (df['typ_vykonu']=='T')]

    print('Loaded (vykony):', len(df))
    return df


def load_vsetku_starostlivost(rok):
    return pd.read_csv(
        DATA_PATH / "01_Všetka starostlivosť" / f"osn_vsetka_starostlivost_{rok}.csv",
        sep=";",
        dtype=defaultdict(
            lambda: "str",
            kod_zp="Int8",
            vek_dni="Int16",
            vek_roky="Int16",
            hmotnost="Int16",
            upv="Int16",
            erv="float",
            osetrovacia_doba="Int16",
        ),
        parse_dates=["datum_od", "datum_do", "datum_narodenia"],
        date_format="ISO8601",
    )


def load_vystup_algoritmu(rok, verzia, prepinace_algoritmu=""):
    _usecols = [0, 7] if verzia.startswith("v2024.2") else [0, 9]
    return pd.read_csv(
        DATA_PATH
        / "07_Algoritmus"
        / f"algoritmus_{verzia}{prepinace_algoritmu}_osn_vsetka_starostlivost_{rok}_output.csv",
        sep=";",
        usecols=_usecols,
        names=["id_hp", "ms"],
        dtype="str",
        header=0,
    )


def load_vsetku_starostlivost_s_ms(rok, verzia):
    return pd.read_csv(
        DATA_PATH
        / "01_Všetka starostlivosť"
        / f"osn_vsetka_starostlivost_{rok}_ms_{verzia}.csv",
        sep=";",
        dtype=defaultdict(
            lambda: "str",
            kod_zp="Int8",
            vek_dni="Int16",
            vek_roky="Int16",
            hmotnost="Int16",
            upv="Int16",
            erv="float",
            osetrovacia_doba="Int16",
        ),
        parse_dates=["datum_od", "datum_do", "datum_narodenia"],
        date_format="ISO8601",
    )
