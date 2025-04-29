"""Temporary file"""

# TODO: Transform it to JSON
from collections import defaultdict

POISTOVNE = {
    "24": {
        "nazov": "dovera",
        "subory": {
            "2021": {
                "uzs_jzs": {
                    "nazvy_suborov": ["2021_24_01_UZS_JZS_UDAJE.csv"],
                    "argumenty": [{"delimiter": ";"}],
                },
                "hp": {
                    "nazvy_suborov": ["2021_24_02_HP_UDAJE.csv"],
                    "argumenty": [
                        {
                            "usecols": [
                                0,
                                1,
                                2,
                                3,
                                4,
                                5,
                                6,
                                8,
                                9,
                                10,
                                11,
                                15,
                                17,
                                18,
                                19,
                                24,
                            ],
                            "names": [
                                "kod_zp",
                                "id_hp_pzs",
                                "id_hp",
                                "pzs_6",
                                "datum_od",
                                "datum_do",
                                "osetrovacia_doba",
                                "vek_dni",
                                "vek_roky",
                                "hmotnost",
                                "upv",
                                "hlavna_diagnoza",
                                "drg",
                                "erv",
                                "zlucene_hp",
                                "typ_starostlivosti",
                            ],
                            "parse_dates": ["datum_od", "datum_do"],
                        },
                    ],
                },
                "preklady": {
                    "nazvy_suborov": ["2021_24_03_HP_PREKLADY.csv"],
                    "argumenty": [
                        {
                            "delimiter": ";",
                            "usecols": [0, 1, 2, 3, 4],
                            "names": [
                                "id_hp",
                                "pzs_12",
                                "datum_od",
                                "datum_do",
                                "kod_zp",
                            ],
                        },
                    ],
                },
                "vdg": {
                    "nazvy_suborov": ["2021_24_04_HP_VDG.csv"],
                    "argumenty": [
                        {
                            "delimiter": ";",
                            "usecols": [0, 1, 3],
                            "names": ["id_hp", "vdg", "kod_zp"],
                        },
                    ],
                },
                "vykony": {
                    "nazvy_suborov": ["2021_24_05_HP_ZV.csv"],
                    "argumenty": [
                        {
                            "delimiter": ";",
                            "usecols": [0, 1, 2, 3, 4],
                            "names": [
                                "id_hp",
                                "kod_vykonu",
                                "lokalizacia_vykonu",
                                "datum_vykonu",
                                "kod_zp",
                            ],
                        },
                    ],
                },
                "poistenci": {
                    "nazvy_suborov": ["2021_24_09_UZS_POISTENCI.csv"],
                    "argumenty": [
                        {
                            "usecols": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                            "names": [
                                "id_poistenca",
                                "datum_narodenia",
                                "pohlavie",
                                "datum_poistenia_od",
                                "datum_poistenia_do",
                                "dovod_ukoncenia",
                                "kod_trvaleho_pobytu",
                                "psc_trvaleho_pobytu",
                                "kod_prechodneho_pobytu",
                                "psc_prechodneho_pobytu",
                                "kod_zp",
                            ],
                        },
                    ],
                },
            },
            "2022": {
                "uzs_jzs": {"nazvy_suborov": ["01_UZS_JZS.csv"], "argumenty": [{}]},
                "hp": {"nazvy_suborov": ["02_HP.csv"], "argumenty": [{}]},
                "preklady": {"nazvy_suborov": ["03_PREKLAD.csv"], "argumenty": [{}]},
                "vdg": {"nazvy_suborov": ["04_VDG.csv"], "argumenty": [{}]},
                "vykony": {"nazvy_suborov": ["05_VYKON.csv"], "argumenty": [{}]},
                "poistenci": {"nazvy_suborov": ["09_poistenci.csv"], "argumenty": [{}]},
            },
            "2023": {
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
    "25": {
        "nazov": "vzp",
        "subory": {
            "2021": {
                "uzs_jzs": {
                    "nazvy_suborov": [
                        "2021_25_01_JZS_UDAJE.csv",
                        "2021_25_01_UZS_UDAJE.csv",
                    ],
                    "argumenty": [
                        {
                            "delimiter": ";",
                            "header": None,
                            "usecols": [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 13, 16, 17],
                            "names": [
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
                                "kod_zp",
                            ],
                        },
                        {
                            "header": None,
                            "usecols": [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 13, 16, 17],
                            "names": [
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
                                "kod_zp",
                            ],
                        },
                    ],
                },
                "hp": {
                    "nazvy_suborov": ["2021_25_02_HP_UDAJE.csv"],
                    "argumenty": [
                        {
                            "header": None,
                            "usecols": [
                                0,
                                1,
                                2,
                                3,
                                4,
                                5,
                                6,
                                8,
                                9,
                                10,
                                11,
                                15,
                                17,
                                18,
                                19,
                                24,
                            ],
                            "names": [
                                "kod_zp",
                                "id_hp_pzs",
                                "id_hp",
                                "pzs_6",
                                "datum_od",
                                "datum_do",
                                "osetrovacia_doba",
                                "vek_dni",
                                "vek_roky",
                                "hmotnost",
                                "upv",
                                "hlavna_diagnoza",
                                "drg",
                                "erv",
                                "zlucene_hp",
                                "typ_starostlivosti",
                            ],
                            "parse_dates": ["datum_od", "datum_do"],
                        },
                    ],
                },
                "preklady": {
                    "nazvy_suborov": ["2021_25_03_HP_PREKLADY.csv"],
                    "argumenty": [
                        {
                            "header": None,
                            "usecols": [0, 1, 2, 3, 4],
                            "names": [
                                "id_hp",
                                "pzs_12",
                                "datum_od",
                                "datum_do",
                                "kod_zp",
                            ],
                        },
                    ],
                },
                "vdg": {
                    "nazvy_suborov": ["2021_25_04_HP_VDG.csv"],
                    "argumenty": [
                        {
                            "header": None,
                            "usecols": [0, 1, 3],
                            "names": ["id_hp", "vdg", "kod_zp"],
                        },
                    ],
                },
                "vykony": {
                    "nazvy_suborov": ["2021_25_05_HP_ZV.csv"],
                    "argumenty": [
                        {
                            "header": None,
                            "usecols": [0, 1, 2, 3, 4],
                            "names": [
                                "id_hp",
                                "kod_vykonu",
                                "lokalizacia_vykonu",
                                "datum_vykonu",
                                "kod_zp",
                            ],
                        },
                    ],
                },
                "poistenci": {
                    "nazvy_suborov": ["2021_25_09_UZS_POISTENCI.csv"],
                    "argumenty": [
                        {
                            "header": None,
                            "usecols": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                            "names": [
                                "id_poistenca",
                                "datum_narodenia",
                                "pohlavie",
                                "datum_poistenia_od",
                                "datum_poistenia_do",
                                "dovod_ukoncenia",
                                "kod_trvaleho_pobytu",
                                "psc_trvaleho_pobytu",
                                "kod_prechodneho_pobytu",
                                "psc_prechodneho_pobytu",
                                "kod_zp",
                            ],
                        },
                    ],
                },
            },
            "2022": {
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
            "2023": {
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
                            "dtype": defaultdict(lambda: "str", pocet="float"),
                        },
                    ],
                },
            },
        },
    },
    "27": {
        "nazov": "union",
        "subory": {
            "2021": {
                "uzs_jzs": {
                    "nazvy_suborov": ["2021_27_01_UZS_JZS_UDAJE.csv"],
                    "argumenty": [
                        {
                            "delimiter": ";",
                            "usecols": [0, 1, 2, 3, 5, 6, 8, 9, 10, 11, 13, 16, 17],
                            "names": [
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
                                "kod_zp",
                            ],
                        },
                    ],
                },
                "hp": {
                    "nazvy_suborov": ["2021_27_02_HP_UDAJE.csv"],
                    "argumenty": [
                        {
                            "usecols": [
                                0,
                                1,
                                2,
                                3,
                                4,
                                5,
                                6,
                                8,
                                9,
                                10,
                                11,
                                15,
                                17,
                                18,
                                19,
                                24,
                            ],
                            "names": [
                                "kod_zp",
                                "id_hp_pzs",
                                "id_hp",
                                "pzs_6",
                                "datum_od",
                                "datum_do",
                                "osetrovacia_doba",
                                "vek_dni",
                                "vek_roky",
                                "hmotnost",
                                "upv",
                                "hlavna_diagnoza",
                                "drg",
                                "erv",
                                "zlucene_hp",
                                "typ_starostlivosti",
                            ],
                            "parse_dates": ["datum_od", "datum_do"],
                        },
                    ],
                },
                "preklady": {
                    "nazvy_suborov": ["2021_27_03_HP_PREKLADY.csv"],
                    "argumenty": [
                        {
                            "usecols": [0, 1, 2, 3, 4],
                            "names": [
                                "id_hp",
                                "pzs_12",
                                "datum_od",
                                "datum_do",
                                "kod_zp",
                            ],
                        },
                    ],
                },
                "vdg": {
                    "nazvy_suborov": ["2021_27_04_HP_VDG.csv"],
                    "argumenty": [{"usecols": [0, 1, 3], "names": ["id_hp", "vdg", "kod_zp"]}],
                },
                "vykony": {
                    "nazvy_suborov": ["2021_27_05_HP_ZV.csv"],
                    "argumenty": [
                        {
                            "usecols": [0, 1, 2, 3, 4],
                            "names": [
                                "id_hp",
                                "kod_vykonu",
                                "lokalizacia_vykonu",
                                "datum_vykonu",
                                "kod_zp",
                            ],
                        },
                    ],
                },
                "poistenci": {
                    "nazvy_suborov": ["2021_27_09_UZS_POISTENCI.csv"],
                    "argumenty": [
                        {
                            "delimiter": ";",
                            "usecols": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                            "names": [
                                "id_poistenca",
                                "datum_narodenia",
                                "pohlavie",
                                "datum_poistenia_od",
                                "datum_poistenia_do",
                                "dovod_ukoncenia",
                                "kod_prechodneho_pobytu",
                                "psc_prechodneho_pobytu",
                                "kod_trvaleho_pobytu",
                                "psc_trvaleho_pobytu",
                                "kod_zp",
                            ],
                        },
                    ],
                },
            },
            "2022": {
                "uzs_jzs": {
                    "nazvy_suborov": ["osn_2022_27_01_uzs_jzs.csv"],
                    "argumenty": [
                        {
                            "converters": {
                                "datum_od": "str.strip",
                                "datum_do": "str.strip",
                            },
                        },
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
                                "datum_od": "str.strip",
                                "datum_do": "str.strip",
                                "datum_narodenia": "str.strip",
                            },
                            "decimal": ",",
                        },
                        {
                            "converters": {
                                "datum_od": "str.strip",
                                "datum_do": "str.strip",
                                "datum_narodenia": "str.strip",
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
                    "argumenty": [{"converters": {"datum_narodenia": "str.strip"}}],
                },
            },
            "2023": {
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

POISTIVNE_ARGS = {
    "uzs_jzs": {
        "usecols": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 17],
        "names": [
            "kod_zp",
            "id_poistenca",
            "obdobie",
            "pzs_12",
            "id_hp",
            "novorodenec",
            "datum_od",
            "datum_do",
            "pohyb_poistenca",
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
        "usecols": [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            19,
            20,
            21,
            26,
        ],
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
            "druh_prijatia",
            "dovod_prijatia",
            "dovod_prepustenia",
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
        "usecols": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "names": [
            "kod_zp",
            "id_poistenca",
            "datum_narodenia",
            "pohlavie",
            "datum_poistenia_od",
            "datum_poistenia_do",
            "dovod_ukoncenia",
            "kod_prechodneho_pobytu",
            "psc_prechodneho_pobytu",
            "kod_trvaleho_pobytu",
            "psc_trvaleho_pobytu",
        ],
        "header": 0,
        "dtype": defaultdict(lambda: "str", kod_zp="Int8"),
        "parse_dates": ["datum_narodenia", "datum_poistenia_od", "datum_poistenia_do"],
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
