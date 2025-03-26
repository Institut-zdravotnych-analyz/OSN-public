import re
from pandas import NA, notna, isna
from pathlib import Path
import os


def zjednot_kod(kod):
    return re.sub("[^0-9a-zA-Z]", "", kod).lower() if notna(kod) else kod


def presun_stlpec(df, nazov_stlpca, nova_pozicia):
    df_copy = df.copy()
    df_copy.insert(nova_pozicia, nazov_stlpca, df_copy.pop(nazov_stlpca))
    return df_copy


def ziskaj_data_path():
    if data_path := os.environ.get("OSN_data"):
        return Path(data_path) / "11_Dátové súbory a prevodníky"
    else:
        raise ValueError('V environmentalnej premennej "OSN_data" sa nenachadza cesta k datam.')


def prirad_vekovu_kategoriu(vek_roky):
    if isna(vek_roky):
        return NA
    if vek_roky >= 19:
        return "dospeli"
    elif vek_roky >= 16:
        return "deti_16"
    elif vek_roky >= 7:
        return "deti_7"
    elif vek_roky >= 1:
        return "deti_1"
    else:
        return "deti_0"


def zisti_uroven_ms(hp):
    if isna(hp["vekova_kategoria"]):
        return NA
    nazov_stlpca = f'uroven_ms_{hp["vekova_kategoria"]}'
    return hp[nazov_stlpca]


def rimska_cislica(cislo):
    rimske_cislice = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
    return rimske_cislice[cislo]
