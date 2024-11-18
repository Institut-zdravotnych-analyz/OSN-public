from collections import defaultdict
import pandas as pd
from OSN_common.pomocne_funkcie import ziskaj_data_path


_data_path = ziskaj_data_path()

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


def nacitaj_prevodovy_subor(nazov):
    if subor := _prevodove_subory.get(nazov):
        return pd.read_csv(_data_path / subor["cesta"], **subor["argumenty"])
    else:
        raise ValueError(f"Prevodník s názvom {nazov} neexistuje.")


def nacitaj_zoznam_obci():
    return pd.read_excel(
        _data_path / "03_Prevodníky" / "KÓDY_OBCE.xlsx",
        dtype=defaultdict(
            lambda: "str",
            {"Počet obyvateľov 2021": "Int64"},
        ),
    )


def nacitaj_zoznam_poistencov(rok):
    return pd.read_csv(
        _data_path / "05_Poistenci" / f"poistenci_vyfiltrovani_{rok}.csv",
        sep=";",
        dtype=defaultdict(
            lambda: "str",
            kod_zp="Int8",
        ),
        parse_dates=["datum_narodenia"],
        date_format="ISO8601",
    )


def nacitaj_siet_nemocnic(rok):
    return pd.read_excel(
        _data_path / "08_Nemocnice" / f"siet_nemocnic_{rok}.xlsx",
        index_col=[0, 1, 2, 3],
        header=[0, 1, 2],
    )


def nacitaj_zoznam_vykonov(rok):
    return pd.read_csv(
        _data_path / "03_Prevodníky" / f"zoznam_vykonov_{rok}.csv",
        sep=";",
        dtype="str",
        converters={"zoznam_terminalnych_vykonov": eval},
    )


def nacitaj_zoznam_diagnoz(rok):
    return pd.read_csv(
        _data_path / "03_Prevodníky" / f"zoznam_diagnoz_{rok}.csv",
        sep=";",
        converters={"zoznam_koncovych_diagnoz": eval},
    )


def nacitaj_zoznam_nemocnic():
    return pd.read_csv(
        _data_path / "08_Nemocnice" / f"zoznam_nemocnic.csv",
        sep=";",
        dtype=defaultdict(lambda: "str", uroven_nemocnice="Int8"),
    )


def nacitaj_zoznam_ms(verzia):
    return pd.read_csv(
        _data_path
        / "03_Prevodníky"
        / "Vyhláška"
        / f"{verzia}"
        / f"zoznam_ms_{verzia}.csv",
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


def nacitaj_programovy_profil(rok, verzia):
    return pd.read_csv(
        _data_path
        / "03_Prevodníky"
        / "Vyhláška"
        / f"{verzia}"
        / f"programovy_profil_{verzia}_{rok}.csv",
        sep=";",
    )


def nacitaj_vsetku_starostlivost(rok):
    return pd.read_csv(
        _data_path / "01_Všetka starostlivosť" / f"osn_vsetka_starostlivost_{rok}.csv",
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


def nacitaj_vystup_algoritmu(rok, verzia, prepinace_algoritmu=""):
    _usecols = [0, 7] if verzia.startswith("v2024.2") else [0, 9]
    return pd.read_csv(
        _data_path
        / "07_Algoritmus"
        / f"algoritmus_{verzia}{prepinace_algoritmu}_osn_vsetka_starostlivost_{rok}_output.csv",
        sep=";",
        usecols=_usecols,
        names=["id_hp", "ms"],
        dtype="str",
        header=0,
    )


def nacitaj_vsetku_starostlivost_s_ms(rok, verzia):
    return pd.read_csv(
        _data_path
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


_predvolene_argumenty_nacitania = {
    "uzs_jzs": {
        "usecols": [0, 1, 2, 3, 4, 6, 7, 9, 10, 11, 12, 14, 17],
        "names": [
            "kod_zp",
            "id_poistenca",
            "obdobie",
            "pzs_12",
            "id_hp",
            "datum_od",
            "datum_do",
            "dgn_prijem",
            "dgn_prepustenie",
            "kod_jednodnoveho_vykonu",
            "kod_operacneho_vykonu",
            "typ_hospitalizacie",
            "typ_starostlivosti",
        ],
        "header": 0,
        "dtype": defaultdict(lambda: "str", kod_zp="Int8"),
        "parse_dates": ["datum_od", "datum_do"],
        "date_format": "ISO8601",
        "delimiter": "|",
    },
    "hp": {
        "usecols": [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 17, 19, 20, 21, 26],
        "names": [
            "kod_zp",
            "id_hp_pzs",
            "id_hp",
            "id_poistenca",
            "pzs_6",
            "datum_od",
            "datum_do",
            "osetrovacia_doba",
            "vek_dni",
            "vek_roky",
            "hmotnost",
            "upv",
            "datum_narodenia",
            "hlavna_diagnoza",
            "drg",
            "erv",
            "zlucene_hp",
            "typ_starostlivosti",
        ],
        "header": 0,
        "dtype": defaultdict(
            lambda: "str",
            kod_zp="Int8",
            osetrovacia_doba="Int16",
            vek_dni="Int16",
            vek_roky="Int16",
            hmotnost="Int16",
            upv="Int16",
            erv="float",
        ),
        "parse_dates": ["datum_od", "datum_do", "datum_narodenia"],
        "date_format": "ISO8601",
        "delimiter": "|",
    },
    "preklady": {
        "usecols": [0, 1, 2, 3, 4],
        "names": ["kod_zp", "id_hp", "pzs_12", "datum_od", "datum_do"],
        "header": 0,
        "dtype": defaultdict(lambda: "str", kod_zp="Int8"),
        "delimiter": "|",
    },
    "vdg": {
        "usecols": [0, 1, 2],
        "names": ["kod_zp", "id_hp", "vdg"],
        "header": 0,
        "dtype": defaultdict(lambda: "str", kod_zp="Int8"),
        "delimiter": "|",
    },
    "vykony": {
        "usecols": [0, 1, 2, 3, 4],
        "names": [
            "kod_zp",
            "id_hp",
            "kod_vykonu",
            "lokalizacia_vykonu",
            "datum_vykonu",
        ],
        "header": 0,
        "dtype": defaultdict(lambda: "str", kod_zp="Int8"),
        "delimiter": "|",
    },
    "poistenci": {
        "usecols": [0, 1, 2, 3, 7, 8, 9, 10],
        "names": [
            "kod_zp",
            "id_poistenca",
            "datum_narodenia",
            "pohlavie",
            "kod_prechodneho_pobytu",
            "psc_prechodneho_pobytu",
            "kod_trvaleho_pobytu",
            "psc_trvaleho_pobytu",
        ],
        "header": 0,
        "dtype": defaultdict(lambda: "str", kod_zp="Int8"),
        "parse_dates": ["datum_narodenia"],
        "date_format": "ISO8601",
        "delimiter": "|",
    },
    "sumar": {
        "usecols": [0, 1, 2, 3],
        "names": ["kod_zp", "pzs_6", "typ_starostlivosti", "pocet"],
        "header": 0,
        "dtype": defaultdict(lambda: "str", kod_zp="Int8", pocet="Int32"),
        "delimiter": "|",
    },
}

_poistovne = {
    24: {
        "nazov": "dovera",
        "subory": {
            2022: {
                "uzs_jzs": {"nazvy_suborov": ["01_UZS_JZS.csv"], "argumenty": [{}]},
                "hp": {"nazvy_suborov": ["02_HP.csv"], "argumenty": [{}]},
                "preklady": {"nazvy_suborov": ["03_PREKLAD.csv"], "argumenty": [{}]},
                "vdg": {"nazvy_suborov": ["04_VDG.csv"], "argumenty": [{}]},
                "vykony": {"nazvy_suborov": ["05_VYKON.csv"], "argumenty": [{}]},
                "poistenci": {"nazvy_suborov": ["09_poistenci.csv"], "argumenty": [{}]},
            },
            2023: {
                "uzs_jzs": {
                    "nazvy_suborov": ["2023_24_01_UZS_JZS_oprava.csv"],
                    "argumenty": [{}],
                },
                "hp": {
                    "nazvy_suborov": ["2023_24_02_HP_oprava.csv"],
                    "argumenty": [{}],
                },
                "preklady": {
                    "nazvy_suborov": ["2023_24_03_PREKLAD_oprava.csv"],
                    "argumenty": [{}],
                },
                "vdg": {"nazvy_suborov": ["2023_24_04_VDG.csv"], "argumenty": [{}]},
                "vykony": {
                    "nazvy_suborov": ["2023_24_05_VYKON.csv"],
                    "argumenty": [{}],
                },
                "poistenci": {
                    "nazvy_suborov": ["2023_24_09_POISTENCI_oprava.csv"],
                    "argumenty": [{}],
                },
                "sumar": {"nazvy_suborov": ["2023_24_13_SUMAR.csv"], "argumenty": [{}]},
            },
        },
    },
    25: {
        "nazov": "vzp",
        "subory": {
            2022: {
                "uzs_jzs": {
                    "nazvy_suborov": ["2022_25_01_UZS_JZS.csv"],
                    "argumenty": [{"header": None}],
                },
                "hp": {
                    "nazvy_suborov": ["2022_25_02_HP.csv"],
                    "argumenty": [{"header": None}],
                },
                "preklady": {
                    "nazvy_suborov": ["2022_25_03_PREKLAD.csv"],
                    "argumenty": [{"header": None}],
                },
                "vdg": {
                    "nazvy_suborov": ["2022_25_04_VDG.csv"],
                    "argumenty": [{"header": None}],
                },
                "vykony": {
                    "nazvy_suborov": ["2022_25_05_VYKON.csv"],
                    "argumenty": [{"header": None}],
                },
                "poistenci": {
                    "nazvy_suborov": ["2022_25_09_POISTENCI.csv"],
                    "argumenty": [{"header": None}],
                },
            },
            2023: {
                "uzs_jzs": {
                    "nazvy_suborov": ["2023_25_01_UZS_JZS_oprava.csv"],
                    "argumenty": [{}],
                },
                "hp": {
                    "nazvy_suborov": ["2023_25_02_HP_oprava.csv"],
                    "argumenty": [{}],
                },
                "preklady": {
                    "nazvy_suborov": ["2023_25_03_PREKLAD.csv"],
                    "argumenty": [{}],
                },
                "vdg": {"nazvy_suborov": ["2023_25_04_VDG.csv"], "argumenty": [{}]},
                "vykony": {
                    "nazvy_suborov": ["2023_25_05_VYKON.csv"],
                    "argumenty": [{}],
                },
                "poistenci": {
                    "nazvy_suborov": [
                        "2023_25_09_POISTENCI_oprava.csv",
                        "2023_25_09_POISTENCI_doplnenie.csv",
                    ],
                    "argumenty": [{}, {}],
                },
                "sumar": {
                    "nazvy_suborov": ["2023_25_13_SUMAR.csv"],
                    "argumenty": [
                        {
                            "usecols": [0, 1, 2],
                            "names": ["pzs_6", "typ_starostlivosti", "pocet"],
                            "dtype": defaultdict(
                                lambda: "str", kod_zp="Int8", pocet="float"
                            ),
                        }
                    ],
                },
            },
        },
    },
    27: {
        "nazov": "union",
        "subory": {
            2022: {
                "uzs_jzs": {
                    "nazvy_suborov": ["osn_2022_27_01_uzs_jzs.csv"],
                    "argumenty": [
                        {"converters": {"datum_od": str.strip, "datum_do": str.strip}}
                    ],
                },
                "hp": {
                    "nazvy_suborov": [
                        "osn_2022_27_02_hp.csv",
                        "osn_nonDRG_2022_27_02_hp.csv",
                    ],
                    "argumenty": [
                        {
                            "converters": {
                                "datum_od": str.strip,
                                "datum_do": str.strip,
                                "datum_narodenia": str.strip,
                            },
                            "decimal": ",",
                        },
                        {
                            "converters": {
                                "datum_od": str.strip,
                                "datum_do": str.strip,
                                "datum_narodenia": str.strip,
                            },
                            "decimal": ",",
                            "usecols": [
                                0,
                                1,
                                2,
                                3,
                                4,
                                6,
                                7,
                                10,
                                11,
                                12,
                                13,
                                14,
                                18,
                                20,
                                21,
                                22,
                                27,
                            ],
                        },
                    ],
                },
                "preklady": {
                    "nazvy_suborov": [
                        "osn_2022_27_03_preklad.csv",
                        "osn_nonDRG_2022_27_03_preklad.csv",
                    ],
                    "argumenty": [{}, {}],
                },
                "vdg": {
                    "nazvy_suborov": [
                        "osn_2022_27_04_vdg.csv",
                        "osn_nonDRG_2022_27_04_vdg.csv",
                    ],
                    "argumenty": [{}, {}],
                },
                "vykony": {
                    "nazvy_suborov": [
                        "osn_2022_27_05_vykon.csv",
                        "osn_nonDRG_2022_27_05_vykon.csv",
                    ],
                    "argumenty": [{}, {}],
                },
                "poistenci": {
                    "nazvy_suborov": ["osn_2022_27_09_poistenci.csv"],
                    "argumenty": [{"converters": {"datum_narodenia": str.strip}}],
                },
            },
            2023: {
                "uzs_jzs": {
                    "nazvy_suborov": ["2023_27_01_UZS_JZS_oprava.csv"],
                    "argumenty": [{}],
                },
                "hp": {
                    "nazvy_suborov": ["2023_27_02_HP_oprava.csv"],
                    "argumenty": [{"decimal": ","}],
                },
                "preklady": {
                    "nazvy_suborov": ["2023_27_03_PREKLAD_oprava.csv"],
                    "argumenty": [{}],
                },
                "vdg": {
                    "nazvy_suborov": ["2023_27_04_VDG_oprava.csv"],
                    "argumenty": [{}],
                },
                "vykony": {
                    "nazvy_suborov": ["2023_27_05_VYKON_oprava.csv"],
                    "argumenty": [{}],
                },
                "poistenci": {
                    "nazvy_suborov": ["2023_27_09_POISTENCI_oprava.csv"],
                    "argumenty": [{}],
                },
                "sumar": {
                    "nazvy_suborov": ["2023_27_13_SUMAR_oprava.csv"],
                    "argumenty": [{}],
                },
            },
        },
    },
}


def nacitaj_data_zp(rok, zoznam_zp):
    data = {}
    for kod in zoznam_zp:
        print(f'Nacitavam data pre poistovnu {_poistovne[kod]["nazov"]}')

        datove_subory = (
            _data_path / "06_Dáta od zdravotných poisťovní" / str(rok) / str(kod)
        )

        data[kod] = {}

        for data_name, data_structure in _poistovne[kod]["subory"][rok].items():
            data[kod][data_name] = pd.DataFrame()

            for _i in range(len(data_structure["nazvy_suborov"])):

                nazov_suboru = data_structure["nazvy_suborov"][_i]
                argumenty = (
                    _predvolene_argumenty_nacitania[data_name]
                    | data_structure["argumenty"][_i]
                )

                print(f"Nacitavam data zo suboru {nazov_suboru}")
                df = pd.read_csv(datove_subory / nazov_suboru, **argumenty)

                stripped = (
                    df.select_dtypes(include="object")
                    .apply(lambda col: col.str.strip())
                    .replace("", pd.NA)
                )
                df.loc[:, stripped.columns] = stripped

                if "kod_zp" not in df.columns:
                    df.insert(0, "kod_zp", kod)

                data[kod][data_name] = pd.concat(
                    [data[kod][data_name], df], ignore_index=True
                )

    return data
