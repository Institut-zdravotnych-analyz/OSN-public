import pandera.pandas as pa
import pandas as pd

# Table 1: ÚSTAVNÁ A JEDNODŇOVÁ STAROSTLIVOSŤ
schema_01_UZS_JZS = pa.DataFrameSchema(
    {
        "KOD_ZP": pa.Column(str, checks=pa.Check.isin(["24", "25", "27"])),
        "BIC_POI": pa.Column(str, checks=pa.Check.str_length(1, 20)),
        "ROK_MESIAC": pa.Column(pa.DateTime, coerce=True, checks=pa.Check.le(pd.to_datetime("2024-12-31"))),
        "PZS_12": pa.Column(str, checks=pa.Check.str_length(12, 12)),
        "ID_HP_ZP": pa.Column(
            str,
            checks=[
                pa.Check.str_length(1, 20),
                pa.Check(lambda g: g[].notna(), groupby="STAROST_TYP"),
            ],
            nullable=True,
        ),
        "NOVORODENEC": pa.Column(str, checks=pa.Check.str_length(3), nullable=False),
        "DATUM_OD": pa.Column(pa.DateTime),
        "DATUM_DO": pa.Column(pa.DateTime),
        "POHYB_POI": pa.Column(str, checks=pa.Check.str_length(4)),
        "DGN_PRIJ": pa.Column(str, checks=pa.Check.str_length(5)),
        "DGN_PREP": pa.Column(str, checks=pa.Check.str_length(5)),
        "KOD_VYKON_JZS": pa.Column(str, checks=pa.Check.str_length(7)),
        "KOD_HZV": pa.Column(str, checks=pa.Check.str_length(7)),
        "HOSP_TYP": pa.Column(str, checks=pa.Check.str_length(1)),
        "PZS_ODOSIELATEL": pa.Column(str, checks=pa.Check.str_length(12)),
        "DATUM_ZIAD": pa.Column(pa.DateTime),
        "STAROST_TYP": pa.Column(str, checks=pa.Check.str_length(3)),
        "ID_CL": pa.Column(str, checks=pa.Check.str_length(15)),
        "UHRADA_HP": pa.Column(pa.Float),
        "UHRADA_PP": pa.Column(pa.Float),
        "UHRADA_IMZS": pa.Column(pa.Float),
        "UHRADA_EMZS": pa.Column(pa.Float),
        "KOD_MS": pa.Column(str, checks=pa.Check.str_length(5)),
        "UROVEN_MS": pa.Column(pa.Int),
        "KOD_PROG": pa.Column(pa.Int),
    }
)

# Table 2: HOSPITALIZAČNÉ PRÍPADY
schema_02_HP = pa.DataFrameSchema(
    {
        "KOD_ZP": pa.Column(str, checks=pa.Check.str_length(2)),
        "ID_HP_PZS": pa.Column(str, checks=pa.Check.str_length(9)),
        "ID_HP_ZP": pa.Column(str, checks=pa.Check.str_length(20)),
        "BIC_POI": pa.Column(str, checks=pa.Check.str_length(20)),
        "PZS_6": pa.Column(str, checks=pa.Check.str_length(6)),
        "DATUM_OD": pa.Column(pa.DateTime),
        "DATUM_DO": pa.Column(pa.DateTime),
        "HP_DLZKA": pa.Column(pa.Int),
        "PRIEPUSTKA_DNI": pa.Column(pa.Int),
        "VEK_DNI": pa.Column(pa.Int),
        "VEK_ROKY": pa.Column(pa.Int),
        "HMOTNOST": pa.Column(pa.Int),
        "UPV_DLZKA": pa.Column(pa.Int),
        "DATUM_NAROD": pa.Column(pa.DateTime),
        "PRIJ_DRUH": pa.Column(pa.Int),
        "PRIJ_DOVOD": pa.Column(pa.Int),
        "PREP_DOVOD": pa.Column(pa.Int),
        "HDG": pa.Column(str, checks=pa.Check.str_length(5)),
        "HDG_LOK": pa.Column(str, checks=pa.Check.str_length(1)),
        "DRG_SKUP": pa.Column(str, checks=pa.Check.str_length(5)),
        "DRG_ERV": pa.Column(pa.Float),
        "ZLUCENE_HP": pa.Column(str, checks=pa.Check.str_length(250)),
        "UHRADA_HP": pa.Column(pa.Float),
        "UHRADA_PP": pa.Column(pa.Float),
        "UHRADA_IMZS": pa.Column(pa.Float),
        "UHRADA_EMZS": pa.Column(pa.Float),
        "STAROST_TYP": pa.Column(str, checks=pa.Check.str_length(3)),
        "KONTRAKT": pa.Column(str, checks=pa.Check.str_length(4)),
    }
)

# Table 3: PREKLADY
schema_03_PREKLAD = pa.DataFrameSchema(
    {
        "KOD_ZP": pa.Column(str, checks=pa.Check.str_length(2)),
        "ID_HP_ZP": pa.Column(str, checks=pa.Check.str_length(20)),
        "PZS_12": pa.Column(str, checks=pa.Check.str_length(12)),
        "DATUM_OD": pa.Column(pa.DateTime),
        "DATUM_DO": pa.Column(pa.DateTime),
    }
)

# Table 4: AKCEPTOVANÉ VEDĽAJŠIE DIAGNÓZY
schema_04_VDG = pa.DataFrameSchema(
    {
        "KOD_ZP": pa.Column(str, checks=pa.Check.str_length(2)),
        "ID_HP_ZP": pa.Column(str, checks=pa.Check.str_length(20)),
        "VDG": pa.Column(str, checks=pa.Check.str_length(5)),
        "VDG_LOK": pa.Column(str, checks=pa.Check.str_length(1)),
    }
)

# Table 5: AKCEPTOVANÉ VÝKONY
schema_05_VYKON = pa.DataFrameSchema(
    {
        "KOD_ZP": pa.Column(str, checks=pa.Check.str_length(2)),
        "ID_HP_ZP": pa.Column(str, checks=pa.Check.str_length(20)),
        "KOD_VYKON": pa.Column(str, checks=pa.Check.str_length(7)),
        "VYKON_LOKAL": pa.Column(str, checks=pa.Check.str_length(1)),
        "DATUM_VYKON": pa.Column(pa.DateTime),
        "VYKON_LEKAR": pa.Column(str, nullable=True, checks=pa.Check.str_length(9)),
    }
)

# Table 6: AKCEPTOVANÉ PRIPOČÍTATEĽNÉ POLOŽKY DRG
schema_06_PPDRG = pa.DataFrameSchema(
    {
        "KOD_ZP": pa.Column(str, checks=pa.Check.str_length(2)),
        "ID_HP_ZP": pa.Column(str, checks=pa.Check.str_length(20)),
        "KOD_PP": pa.Column(str, checks=pa.Check.str_length(7)),
        "CENA_PP": pa.Column(pa.Float),
    }
)

# Table 7: AKCEPTOVANÉ PRIPOČÍTATEĽNÉ POLOŽKY (PÔVODNÉ)
schema_07_PP = pa.DataFrameSchema(
    {
        "KOD_ZP": pa.Column(str, checks=pa.Check.str_length(2)),
        "ID_HP_ZP": pa.Column(str, checks=pa.Check.str_length(20)),
        "PZS_12": pa.Column(str, checks=pa.Check.str_length(12)),
        "DATUM": pa.Column(pa.DateTime),
        "KOD_PP": pa.Column(str, checks=pa.Check.str_length(7)),
        "MNOZSTVO_PP": pa.Column(pa.Float),
        "CENA_PP": pa.Column(pa.Float),
    }
)

# Table 8: IMZS, EMZS
schema_08_IMZS_EMZS = pa.DataFrameSchema(
    {
        "KOD_ZP": pa.Column(str, checks=pa.Check.str_length(2)),
        "ID_HP_ZP": pa.Column(str, checks=pa.Check.str_length(20)),
        "DRUH_ZS": pa.Column(str, checks=pa.Check.str_length(4)),
        "ODB": pa.Column(str, checks=pa.Check.str_length(3)),
        "KOD_VYKON": pa.Column(str, checks=pa.Check.str_length(7)),
        "MNOZSTVO": pa.Column(pa.Float),
        "UHRADA_ZP": pa.Column(pa.Float),
    }
)

# Table 9: ÚDAJE Z REGISTRA POISTENCOV
schema_09_POISTENCI = pa.DataFrameSchema(
    {
        "KOD_ZP": pa.Column(str, checks=pa.Check.str_length(2)),
        "BIC_POI": pa.Column(str, checks=pa.Check.str_length(20)),
        "DATUM_NAROD": pa.Column(pa.DateTime),
        "POHLAVIE": pa.Column(str, checks=pa.Check.str_length(3)),
        "DATUM_POI_OD": pa.Column(pa.DateTime),
        "DATUM_POI_DO": pa.Column(pa.DateTime),
        "KONIEC_POI_DOVOD": pa.Column(str, checks=pa.Check.str_length(2)),
        "KOD_PRECHOD": pa.Column(str, nullable=True, checks=pa.Check.str_length(7)),
        "PSC_PRECHOD": pa.Column(str, nullable=True, checks=pa.Check.str_length(5)),
        "KOD_TRVALY": pa.Column(str, nullable=True, checks=pa.Check.str_length(7)),
        "PSC_TRVALY": pa.Column(str, nullable=True, checks=pa.Check.str_length(5)),
    }
)

# Table 10: ÚDAJE ZO ZOZNAMU ČAKAJÚCICH POISTENCOV
schema_10_CAKAJUCI = pa.DataFrameSchema(
    {
        "KOD_ZP": pa.Column(str, checks=pa.Check.str_length(2)),
        "ID_CL": pa.Column(str, checks=pa.Check.str_length(15)),
        "BIC_POI": pa.Column(str, checks=pa.Check.str_length(20)),
        "DATUM_VYH": pa.Column(pa.DateTime),
        "PZS_12": pa.Column(str, checks=pa.Check.str_length(12)),
        "DATUM_ODO": pa.Column(pa.DateTime),
        "KOD_ODO": pa.Column(str, checks=pa.Check.str_length(7)),
        "DAT_PLAN_POSK": pa.Column(pa.DateTime),
        "KOD_HDG": pa.Column(str, checks=pa.Check.str_length(5)),
        "LOK_HDG": pa.Column(str, checks=pa.Check.str_length(1)),
        "KOD_HZV": pa.Column(str, checks=pa.Check.str_length(7)),
        "KOD_MS": pa.Column(str, checks=pa.Check.str_length(5)),
        "KOD_PROG": pa.Column(str, checks=pa.Check.str_length(2)),
        "DATUM_CAKA_DO": pa.Column(pa.DateTime),
        "KONIEC_CAKA_DOVOD": pa.Column(str, checks=pa.Check.str_length(20)),
        "ID_HP": pa.Column(str, checks=pa.Check.str_length(9)),
        "DATUM_PLAN": pa.Column(pa.DateTime),
        "DOVOD_PREK": pa.Column(str, checks=pa.Check.str_length(1)),
        "SUM_PRER": pa.Column(pa.Int),
        "ID_CL_PRED": pa.Column(str, checks=pa.Check.str_length(15)),
        "NENASTUP": pa.Column(str, checks=pa.Check.str_length(1)),
        "SUHLAS_POI": pa.Column(pa.Int),
        "STAV_CL": pa.Column(str, checks=pa.Check.str_length(1)),
        "DATUM_CAKA_OD": pa.Column(pa.DateTime),
    }
)

# Table 11: ÚDAJE O POČTE MEDICÍNSKYCH SLUŽIEB V RÁMCI PLÁNOVANEJ STAROSTLIVOSTI
schema_11_PLANOVANE_SLUZBY = pa.DataFrameSchema(
    {
        "KOD_ZP": pa.Column(str, checks=pa.Check.str_length(2)),
        "KOD_MS": pa.Column(str, checks=pa.Check.str_length(5)),
        "PZS_12": pa.Column(str, checks=pa.Check.str_length(12)),
        "POCET_MS": pa.Column(pa.Int),
    }
)

# Table 12: ÚDAJE O ZMLUVNÝCH NEPOVINNÝCH PROGRAMOCH
schema_12_ZML_NEPOVINNE_PROGRAMY = pa.DataFrameSchema(
    {
        "KOD_ZP": pa.Column(str, checks=pa.Check.str_length(2)),
        "PZS_12": pa.Column(str, checks=pa.Check.str_length(12)),
        "KOD_PROG": pa.Column(str, checks=pa.Check.str_length(2)),
        "UROVEN_MS": pa.Column(pa.Int),
        "DAT_OD": pa.Column(pa.DateTime),
        "DAT_DO": pa.Column(pa.DateTime),
    }
)

# Table 13: ÚDAJE O KVALITE
schema_13_KVALITA = pa.DataFrameSchema(
    {
        "KOD_ZP": pa.Column(str, checks=pa.Check.str_length(2)),
        "PZS_6": pa.Column(str, checks=pa.Check.str_length(12)),
        "IK": pa.Column(str, checks=pa.Check.str_length(4)),
        "HODNOTA_C_IK": pa.Column(pa.Float),
        "HODNOTA_M_IK": pa.Column(pa.Float),
    }
)

# Table 14: SUMÁRNE ÚDAJE ZA PÚZS A HOSPITALIZAČNÉ PRÍPADY
schema_14_SUMAR = pa.DataFrameSchema(
    {
        "KOD_ZP": pa.Column(str, checks=pa.Check.str_length(2)),
        "PZS_6": pa.Column(str, checks=pa.Check.str_length(6)),
        "STAROST_TYP": pa.Column(str, checks=pa.Check.str_length(3)),
        "POCET_TYP": pa.Column(pa.Int),
        "UHRADA_HP": pa.Column(pa.Float),
        "UHRADA_PP": pa.Column(pa.Float),
        "UHRADA_IMZS": pa.Column(pa.Float),
        "UHRADA_EMZS": pa.Column(pa.Float),
    }
)

if __name__ == "__main__":
    from OSN_common.helpers import norm_path
    from pathlib import Path
    import os

    df_path = norm_path(
        Path(os.environ.get("OSN_data"))
        / "11_Dátové súbory a prevodníky"
        / "06_Dáta od zdravotných poisťovní"
        / "2024"
        / "24"
        / "2024_24_01_UZS_JZS.csv"
    )

    df = pd.read_csv(df_path, sep="|", dtype=str)

    try:
        schema_01_UZS_JZS.validate(df)
    except pa.errors.SchemaError as exc:
        print(exc)
