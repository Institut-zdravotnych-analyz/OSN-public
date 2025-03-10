from collections import defaultdict

### LOGGER

LOG_COLOR_SCHEME = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "white,bg_red",
}

LOG_FMT_FILE = "%(asctime)s %(levelname)8s -- %(message)s"
LOG_FMT_CONSOLE = "%(log_color)s%(asctime)s %(levelname)8s -- %(reset)s%(white)s%(message)s"

### CONVERTERS

INT_2_ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
ROMAN_2_INT = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5}

### PRILOHY - USEFUL COLS

P1_MAIN_COLS = ["cislo_programu", "nazov_programu", "uroven_programu"]

P1_POVINNOSTI_P_COLS = [
    "povinnost_programu_V",
    "povinnost_programu_IV",
    "povinnost_programu_III",
    "povinnost_programu_II",
    "povinnost_programu_I",
]

P1_DATE_COLS = ["od", "do"]

P2_MAIN_COLS = ["cislo_programu", "kod_ms", "zdielana_ms", "nazov_ms", "sposob_urcenia"]

P2_UROVNE_COLS = ["uroven_ms_dospeli", "uroven_ms_deti_0", "uroven_ms_deti_1", "uroven_ms_deti_7", "uroven_ms_deti_16"]

P2_POVINNOSTI_MS_COLS = [
    "povinnost_ms_V",
    "povinnost_ms_IV",
    "povinnost_ms_III",
    "povinnost_ms_II",
    "povinnost_ms_I",
]

P2_NUM_COLS = ["casova_dostupnost", "minimum_na_nemocnicu", "minimum_na_lekara"]


# PRILOHY XLSX
class PrilohyXlsxMeta:
    P1 = {
        "columns": P1_MAIN_COLS + P1_POVINNOSTI_P_COLS + P1_DATE_COLS,
        "footer": {
            "P": "povinný program podľa § 2 ods. 17 zákona, program príslušnej úrovne je povinný v danej úrovni nemocnice",
            "D": "doplnkový program podľa § 2 ods. 19 zákona, program príslušnej úrovne môže nemocnica danej úrovne poskytovať ako doplnkový, a to na základe povolenia Komisie pre tvorbu siete pri vyhodnotení potreby v regióne",
            "N": "nepovinný program podľa § 2 ods. 18 zákona, program príslušnej úrovne je nepovinný v danej úrovni nemocnice, nemocnica ho môže poskytovať na základe zmluvy so zdravotnou poisťovňou",
        },
        "file": "01_Programovy profil.xlsx",
        "order": 1,
        "title": "Programový profil pre každú úroveň nemocnice",
    }

    P2 = {
        "columns": P2_MAIN_COLS + P2_UROVNE_COLS + P2_POVINNOSTI_MS_COLS + P2_NUM_COLS,
        "columns_full": [
            "Číslo programu",
            "Kód medicínskej služby",
            "Zdieľaná medicínska služba",
            "Názov medicínskej služby",
            "Spôsob určenia",
            "Uroveň dospelí",
            "Uroveň deti do 1r",
            "Uroveň deti 1-6r",
            "Uroveň deti 7-15r",
            "Uroveň deti 16-18r",
            "Povinnosť V.",
            "Povinnosť IV.",
            "Povinnosť III.",
            "Povinnosť II.",
            "Povinnosť I.",
            "Časová dostupnosť",
            "Minimum na nemocnicu",
            "Minimum na lekára",
        ],
        "column_widths": {
            "A": 5.43,
            "B": 7.43,
            "C": 7.43,
            "D": 60.43,
            "E": 7.43,
            "F": 4.43,
            "G": 4.43,
            "H": 4.43,
            "I": 4.43,
            "J": 4.43,
            "K": 4.43,
            "L": 4.43,
            "M": 4.43,
            "N": 4.43,
            "O": 4.43,
            "P": 4.71,
            "Q": 10.5,
            "R": 10.5,
            "S": 15,  # diff
        },
        "description": "",
        "diff_translations": {"added": "Nová MS", "removed": "Odstránená MS", "edited": "Upravená MS", "same": ""},
        "file": "02_Zoznam-medicinskych-sluzieb.xlsx",
        "order": 2,
        "title": "Zoznam medicínskych služieb so zaradením do programov a podmienky pre poskytnutie medicínskych služieb v nemocnici",
    }

    P3 = {
        "file": "03_Personalne zabezpecenie materialno technicke vybavenie a dalsie poziadavky na jednotlive urovne.docx",
        "order": 3,
    }

    P4 = {"file": "04_Indikatory kvality pre ustavnu starostlivost.xlsx", "order": 4}

    P5 = {"file": "05_Sposob urcenia medicinskej sluzby pre novorodencov_NOV.xlsx", "order": 5}

    P6 = {
        "file": "06_Sposob urcenia medicinskej sluzby podla skupiny klasifikacneho systemu a diagnozy_DRGD.xlsx",
        "order": 6,
    }

    P7 = {
        "columns": ["kod_vykonu", "nazov_vykonu", "nazov_ms", "kod_ms"],
        "file": "07_Sposob urcenia medicinskej sluzby podla hlavneho zdravotneho vykonu a zdravotneho vykonu pre deti_VV.xlsx",
        "order": 7,
    }

    P8 = {
        "file": "08_Sposob urcenia medicinskej sluzby podla hlavnho zdravotnho vykonu a zdravotneho vykonu pre dospelych_VV.xlsx",
        "order": 8,
    }

    P9 = {
        "columns": ["kod_hlavneho_vykonu", "nazov_hlavneho_vykonu", "skupina_diagnoz", "kod_ms", "nazov_ms"],
        "file": "09_Sposob urcenie medicinskej sluzby podla hlavneho vykonu a diagnozy_VD.xlsx",
        "order": 9,
    }

    P10 = {
        "columns": ["skupina_diagnoz", "kod_hlavnej_diagnozy", "nazov_hlavnej_diagnozy", "kod_ms", "nazov_ms"],
        "file": "10_Sposob urcenia medicinskej sluzby podla hlavnej a vedlajsej diagnozy_DD.xlsx",
        "order": 10,
    }

    P12 = {
        "order": 12,
        "abbrvs": {
            "AV Shunt": "Artério-venózny shunt",
            "BEVAR": "z anglického branched endovascular aneurysm repair - nemá preklad",
            "CMP": "cievna mozgová príhoda",
            "CT": "výpočtová tomografia",
            "DBS": "hĺbková mozgová stimulácia",
            "EEG": "elektroencefalografia",
            "EKG": "elektrokardiografia",
            "EUG": "extrauterinná gravidita",
            "FEVAR": "z anglického fenestrated endovascular aneurysm repair - nemá preklad",
            "GERD": "gastroezofageálna refluxová choroba",
            "HRCT": "výčtová tomografia s vysokým priestorovým rozlíšením",
            "HSK": "hysteroskopia",
            "CHEVAR": "z anglického chimmey endovascular aneurysm repair - nemá preklad",
            "KP": "koniec panvový",
            "LU": "lymfatická uzlina",
            "MR": "magnetická rezonancia",
            "ORL": "otorinolaryngológia",
            "PKI": "perkutánna koronárna intervencia",
            "pPKI": "primárna perkutánna koronárna intervencia",
            "VAD": "z anglického ventricular assist devices - mechanické podporné systémy srdca",
            "VVCH": "vrodené vývojové chyby",
        },
        "columns": ["kod_vykonu", "nazov_vykonu", "kod_ms", "nazov_ms"],
        "columns_full": ["Kód výkonu", "Zdravotný výkon", "Kód medicínskej služby", "Medicínska služba"],
        "column_widths": {"A": 14.71, "B": 49.71, "C": 19.71, "D": 50.14, "E": 30},
        "description": "Ak bol poistencovi vo veku 18 rokov a menej poskytnutý hlavný zdravotný výkon podľa stĺpca 'zdravotný výkon', hospitalizácii sa určí medicínska služba podľa stĺpca 'medicínska služba' (V).",
        "diff_translations": {
            "added": "Nové zaradenie výkonu",
            "removed": "Odstránené zaradenie výkonu",
            "edited": "Upravené zaradenie výkonu",
            "same": "",
        },
        "file": "12_Sposob urcenia medicinskej sluzby podla hlavneho vykonu pre deti_V.xlsx",
        "footer": {
            "V": "Označenie pre spôsob určenia medicínskej služby, kedy bol poistencovi počas hospitalizácie poskytnutý hlavný zdravotný výkon zo zoznamu v prílohe č.13 alebo č. 14, medicínska služba sa určí podľa prílohy č. 13 alebo č. 14."
        },
        "programs_ordered": [
            48,
            49,
            58,
            3,
            18,
            50,
            51,
            52,
            55,
            22,
            23,
            56,
            57,
            16,
            60,
            11,
            59,
            54,
            53,
            62,
            24,
            64,
            73,
            65,
            70,
            42,
            68,
            66,
            67,
            71,
            72,
            69,
            74,
            61,
            75,
            76,
            45,
            63,
            77,
        ],
        "title": "Spôsob určenia medicínskej služby podľa hlavného výkonu pre poistencov vo veku 18 rokov a menej",
    }

    P13 = {
        **P12,
        "description": "Ak bol poistencovi vo veku viac ako 18 rokov poskytnutý hlavný zdraovotný výkon podľa stĺpca 'zdravotný výkon', hospitalizácii sa určí medicínska služba podľa stĺpca 'medicínska služba' (V).",
        "file": "13_Sposob urcenia medicinskej sluzby podla hlavneho vykonu pre dospelych_V.xlsx",
        "order": 13,
        "programs_ordered": [
            17,
            3,
            18,
            7,
            1,
            2,
            12,
            44,
            8,
            10,
            11,
            9,
            13,
            15,
            19,
            20,
            21,
            22,
            23,
            16,
            6,
            5,
            4,
            14,
            24,
            26,
            37,
            27,
            40,
            41,
            42,
            30,
            28,
            29,
            33,
            35,
            31,
            38,
            32,
            34,
            36,
            39,
            43,
            45,
            25,
            46,
            47,
        ],
        "title": "Spôsob určenia medicínskej služby podľa hlavného výkonu pre poistencov vo veku viac ako 18 rokov",
    }

    P14 = {
        "abbrvs": {
            "AIM": "anestéziológia a intenzívna medicína",
            "CNS": "centrálna nervová sústava",
            "GIT": "gastrointestinálny trakt",
            "NCMP": "náhla cievna mozgová príhoda",
        },
        "columns": ["kod_diagnozy", "nazov_diagnozy", "kod_ms", "nazov_ms"],
        "columns_full": ["Kód diagnózy", "Hlavná diagnóza", "Kód medicínskej služby", "Medicínska služba"],
        "column_widths": {"A": 14.71, "B": 49.71, "C": 19.71, "D": 50.14, "E": 30},
        "description": "Ak bola poistencov vo veku 18 rokov a menej pri hospitalizácii vykázaná hlavná diagnóza podľa stĺpca 'hlavná diagnóza', hospitalizácii sa určí medicínska služba podľa stĺpca 'medicínska služba' (D).",
        "diff_translations": {
            "added": "Nová diagnóza",
            "removed": "Odstránenie diagnózy",
            "edited": "Preradenie diagnózy",
            "same": "",
        },
        "file": "14_Sposob urcenia medicinskej sluzby podla hlavnej diagnozy pre deti_D.xlsx",
        "footer": {
            "D": "Označenie pre spôsob určenia medicínskej služby, kedy sa medicínska služba pre poistencov určí podľa hlavnej diagnózy podľa prílohy č. 14 alebo č. 15; ak hlavná diagnóza pre hospitalizáciu nebola určená poskytovateľom zdravotnej starostlivosti, za hlavnú diagnózu sa považuje diagnóza pri prepustení."
        },
        "order": 14,
        "title": "Spôsob určenia medicínskej služby podľa hlavnej diagnózy pre poistencov vo veku 18 rokov a menej",
    }

    P15 = {
        **P14,
        "description": "Ak bola poistencovi vo veku viac ako 18 rokov pri hospitalizácii vykázaná hlavná diagnóza podľa stĺpca 'hlavná diagnóza', hospitalizácii sa určí medicínska služba podľa stĺpca 'medicínska služba' (D).",
        "file": "15_Sposob urcenia medicinskej sluzby podla hlavnej diagnozy pre dospelych_D.xlsx",
        "order": 15,
        "title": "Spôsob určenia medicínskej služby podľa hlavnej diagnózy pre poistencov vo veku viac ako 18 rokov",
    }

    P16 = {"file": "16_Sposob urcenia medicinskej sluzby podla specialnych pravidiel_S.xlsx", "order": 16}

    P17 = {"file": "17_Sposob urcenia medicinskej sluzby pre program 98.xlsx", "order": 17}


class PrilohyXlsxFormats:
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


# TODO: MOVE TO JSON
POISTOVNE = {
    "24": {
        "nazov": "dovera",
        "subory": {
            "2021": {
                "uzs_jzs": {"nazvy_suborov": ["2021_24_01_UZS_JZS_UDAJE.csv"], "argumenty": [{"delimiter": ";"}]},
                "hp": {
                    "nazvy_suborov": ["2021_24_02_HP_UDAJE.csv"],
                    "argumenty": [
                        {
                            "usecols": [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 15, 17, 18, 19, 24],
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
                        }
                    ],
                },
                "preklady": {
                    "nazvy_suborov": ["2021_24_03_HP_PREKLADY.csv"],
                    "argumenty": [
                        {
                            "delimiter": ";",
                            "usecols": [0, 1, 2, 3, 4],
                            "names": ["id_hp", "pzs_12", "datum_od", "datum_do", "kod_zp"],
                        }
                    ],
                },
                "vdg": {
                    "nazvy_suborov": ["2021_24_04_HP_VDG.csv"],
                    "argumenty": [{"delimiter": ";", "usecols": [0, 1, 3], "names": ["id_hp", "vdg", "kod_zp"]}],
                },
                "vykony": {
                    "nazvy_suborov": ["2021_24_05_HP_ZV.csv"],
                    "argumenty": [
                        {
                            "delimiter": ";",
                            "usecols": [0, 1, 2, 3, 4],
                            "names": ["id_hp", "kod_vykonu", "lokalizacia_vykonu", "datum_vykonu", "kod_zp"],
                        }
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
                        }
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
                "uzs_jzs": {"nazvy_suborov": ["2023_24_01_UZS_JZS_oprava.csv"], "argumenty": [{}]},
                "hp": {"nazvy_suborov": ["2023_24_02_HP_oprava.csv"], "argumenty": [{}]},
                "preklady": {"nazvy_suborov": ["2023_24_03_PREKLAD_oprava.csv"], "argumenty": [{}]},
                "vdg": {"nazvy_suborov": ["2023_24_04_VDG.csv"], "argumenty": [{}]},
                "vykony": {"nazvy_suborov": ["2023_24_05_VYKON.csv"], "argumenty": [{}]},
                "poistenci": {"nazvy_suborov": ["2023_24_09_POISTENCI_oprava.csv"], "argumenty": [{}]},
                "sumar": {"nazvy_suborov": ["2023_24_13_SUMAR.csv"], "argumenty": [{}]},
            },
        },
    },
    "25": {
        "nazov": "vzp",
        "subory": {
            "2021": {
                "uzs_jzs": {
                    "nazvy_suborov": ["2021_25_01_JZS_UDAJE.csv", "2021_25_01_UZS_UDAJE.csv"],
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
                            "usecols": [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 15, 17, 18, 19, 24],
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
                        }
                    ],
                },
                "preklady": {
                    "nazvy_suborov": ["2021_25_03_HP_PREKLADY.csv"],
                    "argumenty": [
                        {
                            "header": None,
                            "usecols": [0, 1, 2, 3, 4],
                            "names": ["id_hp", "pzs_12", "datum_od", "datum_do", "kod_zp"],
                        }
                    ],
                },
                "vdg": {
                    "nazvy_suborov": ["2021_25_04_HP_VDG.csv"],
                    "argumenty": [{"header": None, "usecols": [0, 1, 3], "names": ["id_hp", "vdg", "kod_zp"]}],
                },
                "vykony": {
                    "nazvy_suborov": ["2021_25_05_HP_ZV.csv"],
                    "argumenty": [
                        {
                            "header": None,
                            "usecols": [0, 1, 2, 3, 4],
                            "names": ["id_hp", "kod_vykonu", "lokalizacia_vykonu", "datum_vykonu", "kod_zp"],
                        }
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
                        }
                    ],
                },
            },
            "2022": {
                "uzs_jzs": {"nazvy_suborov": ["2022_25_01_UZS_JZS.csv"], "argumenty": [{"header": None}]},
                "hp": {"nazvy_suborov": ["2022_25_02_HP.csv"], "argumenty": [{"header": None}]},
                "preklady": {"nazvy_suborov": ["2022_25_03_PREKLAD.csv"], "argumenty": [{"header": None}]},
                "vdg": {"nazvy_suborov": ["2022_25_04_VDG.csv"], "argumenty": [{"header": None}]},
                "vykony": {"nazvy_suborov": ["2022_25_05_VYKON.csv"], "argumenty": [{"header": None}]},
                "poistenci": {"nazvy_suborov": ["2022_25_09_POISTENCI.csv"], "argumenty": [{"header": None}]},
            },
            "2023": {
                "uzs_jzs": {"nazvy_suborov": ["2023_25_01_UZS_JZS_oprava.csv"], "argumenty": [{}]},
                "hp": {"nazvy_suborov": ["2023_25_02_HP_oprava.csv"], "argumenty": [{}]},
                "preklady": {"nazvy_suborov": ["2023_25_03_PREKLAD.csv"], "argumenty": [{}]},
                "vdg": {"nazvy_suborov": ["2023_25_04_VDG.csv"], "argumenty": [{}]},
                "vykony": {"nazvy_suborov": ["2023_25_05_VYKON.csv"], "argumenty": [{}]},
                "poistenci": {
                    "nazvy_suborov": ["2023_25_09_POISTENCI_oprava.csv", "2023_25_09_POISTENCI_doplnenie.csv"],
                    "argumenty": [{}, {}],
                },
                "sumar": {
                    "nazvy_suborov": ["2023_25_13_SUMAR.csv"],
                    "argumenty": [
                        {
                            "usecols": [0, 1, 2],
                            "names": ["pzs_6", "typ_starostlivosti", "pocet"],
                            "dtype": ["str", "str", "float"],
                        }
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
                        }
                    ],
                },
                "hp": {
                    "nazvy_suborov": ["2021_27_02_HP_UDAJE.csv"],
                    "argumenty": [
                        {
                            "usecols": [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 15, 17, 18, 19, 24],
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
                        }
                    ],
                },
                "preklady": {
                    "nazvy_suborov": ["2021_27_03_HP_PREKLADY.csv"],
                    "argumenty": [
                        {"usecols": [0, 1, 2, 3, 4], "names": ["id_hp", "pzs_12", "datum_od", "datum_do", "kod_zp"]}
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
                            "names": ["id_hp", "kod_vykonu", "lokalizacia_vykonu", "datum_vykonu", "kod_zp"],
                        }
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
                        }
                    ],
                },
            },
            "2022": {
                "uzs_jzs": {
                    "nazvy_suborov": ["osn_2022_27_01_uzs_jzs.csv"],
                    "argumenty": [{"converters": {"datum_od": "str.strip", "datum_do": "str.strip"}}],
                },
                "hp": {
                    "nazvy_suborov": ["osn_2022_27_02_hp.csv", "osn_nonDRG_2022_27_02_hp.csv"],
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
                            "usecols": [0, 1, 2, 3, 4, 6, 7, 10, 11, 12, 13, 14, 18, 20, 21, 22, 27],
                        },
                    ],
                },
                "preklady": {
                    "nazvy_suborov": ["osn_2022_27_03_preklad.csv", "osn_nonDRG_2022_27_03_preklad.csv"],
                    "argumenty": [{}, {}],
                },
                "vdg": {
                    "nazvy_suborov": ["osn_2022_27_04_vdg.csv", "osn_nonDRG_2022_27_04_vdg.csv"],
                    "argumenty": [{}, {}],
                },
                "vykony": {
                    "nazvy_suborov": ["osn_2022_27_05_vykon.csv", "osn_nonDRG_2022_27_05_vykon.csv"],
                    "argumenty": [{}, {}],
                },
                "poistenci": {
                    "nazvy_suborov": ["osn_2022_27_09_poistenci.csv"],
                    "argumenty": [{"converters": {"datum_narodenia": "str.strip"}}],
                },
            },
            "2023": {
                "uzs_jzs": {"nazvy_suborov": ["2023_27_01_UZS_JZS_oprava.csv"], "argumenty": [{}]},
                "hp": {"nazvy_suborov": ["2023_27_02_HP_oprava.csv"], "argumenty": [{"decimal": ","}]},
                "preklady": {"nazvy_suborov": ["2023_27_03_PREKLAD_oprava.csv"], "argumenty": [{}]},
                "vdg": {"nazvy_suborov": ["2023_27_04_VDG_oprava.csv"], "argumenty": [{}]},
                "vykony": {"nazvy_suborov": ["2023_27_05_VYKON_oprava.csv"], "argumenty": [{}]},
                "poistenci": {"nazvy_suborov": ["2023_27_09_POISTENCI_oprava.csv"], "argumenty": [{}]},
                "sumar": {"nazvy_suborov": ["2023_27_13_SUMAR_oprava.csv"], "argumenty": [{}]},
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
        "usecols": [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 26],
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
        "dtype": ["Int8", "str", "str", "Int32"],
        "delimiter": "|",
    },
}
