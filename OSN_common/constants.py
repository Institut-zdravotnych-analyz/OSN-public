"""Useful constants for repositories OSN-public and OSN-private."""


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

### PRILOHY - USEFUL DATA

FALLBACK_MS = "S99-99"

POVINNOSTI_MS_COLS = [
    "povinnost_ms_V",
    "povinnost_ms_IV",
    "povinnost_ms_III",
    "povinnost_ms_II",
    "povinnost_ms_I",
]

POVINNOSTI_PROG_COLS = [
    "povinnost_programu_V",
    "povinnost_programu_IV",
    "povinnost_programu_III",
    "povinnost_programu_II",
    "povinnost_programu_I",
]

UROVNE_MS_COLS = [
    "uroven_ms_dospeli",
    "uroven_ms_deti_0",
    "uroven_ms_deti_1",
    "uroven_ms_deti_7",
    "uroven_ms_deti_16",
]

# sposob urcenia mapped to Priloha where it could be found
SPOSOB_2_PRILOHA = {
    "D": ["p14", "p15"],
    "DD": ["p10"],
    "DRGD": ["p6"],
    "M": ["p17"],
    "MD": ["p9a"],
    "MV": ["p7a", "p8a"],
    "NOV": ["p5"],
    "S": ["p16"],
    "V": ["p12", "p13"],
    "VD": ["p9"],
    "VV": ["p7", "p8"],
}

SPOSOBY_URCENIA_VALUES = sorted(SPOSOB_2_PRILOHA.keys())


### PRILOHY XLSX
class PrilohyXlsxMeta:
    """Metadata related to Prilohy documents 1 - 17"""

    P1 = {
        "columns": ["cislo_programu", "nazov_programu", "uroven_programu", *POVINNOSTI_PROG_COLS, "od", "do"],
        "columns_full": [
            "Číslo programu",
            "Názov programu",
            "Úroveň programu",
            "Úroveň nemocnice V.",
            "Úroveň nemocnice IV.",
            "Úroveň nemocnice III.",
            "Úroveň nemocnice II.",
            "Úroveň nemocnice I.",
            "Dátum uplatňovania profilu - od",
            "Dátum uplatňovania profilu - do",
        ],
        "file": "01_Programovy profil.xlsx",
        "index": "1",
        "title": "Programový profil pre každú úroveň nemocnice",
        "vysvetlivky": [
            {
                "title": "Vysvetlivky skratiek:",
                "rows": [
                    "P - povinný program podľa § 2 ods. 17 zákona, program príslušnej úrovne je povinný v danej úrovni nemocnice",
                    "D - doplnkový program podľa § 2 ods. 19 zákona, program príslušnej úrovne môže nemocnica danej úrovne poskytovať ako doplnkový, a to na základe povolenia Komisie pre tvorbu siete pri vyhodnotení potreby v regióne",
                    "N - nepovinný program podľa § 2 ods. 18 zákona, program príslušnej úrovne je nepovinný v danej úrovni nemocnice, nemocnica ho môže poskytovať na základe zmluvy so zdravotnou poisťovňou",
                ],
            },
        ],
    }

    P2 = {
        "columns": [
            "cislo_programu",
            "kod_ms",
            "zdielana_ms",
            "nazov_ms",
            "sposob_urcenia",
            *UROVNE_MS_COLS,
            *POVINNOSTI_MS_COLS,
            "casova_dostupnost",
            "minimum_na_nemocnicu",
            "minimum_na_lekara",
        ],
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
            "S": 25,  # diff
        },
        "description": "",
        "diff_translations": {
            "added": "Pridaná MS",
            "removed": "Odstránená MS",
            "edited": "Nová verzia MS",
            "original": "Pôvodná verzia MS",
            "same": "",
        },
        "file": "02_Zoznam-medicinskych-sluzieb.xlsx",
        "headers": ["Príloha č. 2", "k vyhláške č. .../... Z. z."],
        "index": "2",
        "title": "Zoznam medicínskych služieb so zaradením do programov a podmienky pre poskytnutie medicínskych služieb v nemocnici",
        "vysvetlivky": [
            {
                "title": "Vek poistenca:",
                "subtitle": "Vek pacienta sa radí do piatich skupín. Nižšie je presné rozdelenie s počtom rokov a dní:",
                "rows": [
                    "Deti do 1 roka:  od 0 dní do 364 dní",
                    "Deti 1 - 6 rokov: od 1 roka a 0 dní do 6 rokov a 364 dní",
                    "Deti 6 - 15 rokov: od 7 rokov a 0 dní do 15 rokova a 364 dní",
                    "Deti 16-18 rokov: od 16 rokov a 0 dní do 18 rokov a 364 dní",
                    "Dospelí: od 19 rokov a 0 dní",
                ],
            },
            {
                "title": "Úroveň medicínskej služby:",
                "rows": [
                    "1. Dospelí – úroveň medicnskej služby pre pacientov vo veku nad 18 rokov,",
                    "2. Deti do 1r – úroveň medicnskej služby pre pacientov do dovŕšenia 1 roka veku,",
                    "3. Deti 1-6r – úroveň medicnskej služby pre pacientov vo veku 1 až 6 rokov,",
                    "4. Deti 7-15r – úroveň medicskej služby pre pacientov vo veku 7 až 15 rokov,",
                    "5. Deti 16-18r – úroveň medicskej služby pre pacientov vo veku 16 až 18 rokov,",
                ],
            },
            {
                "title": "Zdieľaná medicínska služba:",
                "subtitle": "ZD - zdieľaná medicínska služba, úroveň zdielanej služby určuje medicínsky program, kde je zaradená, ako aj časovú dostupnosť a minimálne počty na nemocnicu a lekára",
            },
            {
                "title": "Spôsob určenia medicínskej služby:",
                "rows": [
                    "a) Hospitalizačný prípad sa spravidla zaraďuje do medicínskej služby a medicínskeho programu až po ukončení hospitalizácie.",
                    "b) V prípade, ak hospitalizačný prípad začal v roku 2023, tento hospitalizačný prípad sa posudzuje podľa začatia hospitalizačného prípadu.To znamená, že sa na tieto hospitalizačné prípady nevzťahuje kategorizácia ústavnej zdravotnej starostlivosti, nakoľko v tom čase nebola účinná.",
                    "c) V prípade platnosti nového právneho predpisu, t. j. kategorizačnej vyhlášky od určitého mesiaca, platí to isté ako pre bod b).",
                ],
            },
            {
                "title": "",
                "rows": [
                    "NOV - Označenie pre spôsob určenia medicínskej služby pre novorodenca, medicínska služba sa určí podľa skupiny klasifikačného systému alebo podľa skupiny klasifikačného systému a zdravotného výkonu alebo diagnózy podľa doplňujúceho kritéria podľa prílohy č. 5.",
                    "DRGD - Označenie pre spôsob určenia medicínskej služby, ak bol hospitalizačný prípad zaradený do skupiny podľa klasifikačného systému začínajúcej na písmeno „W‟, medicínska služba sa určí podľa skupiny klasifikačného systému, do ktorej bol hospitalizačný prípad zaradený, a diagnózy podľa prílohy č. 6.",
                    "VV - Označenie pre spôsob určenia medicínskej služby, ak bol poistencovi počas hospitalizácie poskytnutý v kombinácii hlavný zdravotný výkon a jeden alebo viac zdravotných výkonov zo zoznamu ďalších zdravotných výkonov podľa prílohy č. 7 alebo č. 8, sa medicínska služba určí podľa kombinácie hlavného zdravotného výkonu a vykázaného zdravotného výkonu alebo podľa hlavného zdravotného výkonu a vykázaných zdravotných výkonov podľa prílohy č. 7 alebo č. 8,",
                    "MV - Označenie pre spôsob určenia medicínskej služby, ak bol poistencovi počas hospitalizácie vykázaný marker a minimálne jeden výkon zo zoznamu výkonov podľa prílohy č. 7a alebo č. 8a, medicínska služba sa určí podľa kombinácie markera a vykázaného zdravotného výkonu podľa prílohy č. 7a alebo č. 8a.",
                    "VD - Označenie pre spôsob určenia medicínskej služby, ak bol poistencovi počas hospitalizácie poskytnutý zdravotný výkon pri vykázanej diagnóze, ktorý zodpovedá kombinácii zdravotného výkonu a diagnózy podľa prílohy č. 9, medicínska služba sa určí podľa kombinácie hlavného zdravotného výkonu a diagnózy podľa prílohy č. 9.",
                    "MD - Označenie pre spôsob určenia medicínskej služby, ak bol poistencovi počas hospitalizácie poskytnutý zdravotný výkon pri vykázaní markera, ktorý zodpovedá kombinácii zdravotného výkonu a markera podľa prílohy č. 9a, medicínska služba sa určí podľa kombinácie markera a diagnózy podľa prílohy č. 9a.",
                    "DD - Označenie pre spôsob určenia medicínskej služby, ak bola poistencovi počas hospitalizácie vykázaná kombinácia hlavnej a vedľajšej diagnózy, medicínska služba sa určí podľa kombinácie hlavnej diagnózy a diagnózy podľa prílohy č. 10.",
                    "V - Označenie pre spôsob určenia medicínskej služby, kedy bol poistencovi počas hospitalizácie poskytnutý hlavný zdravotný výkon zo zoznamu v prílohe č. 12 alebo č. 13, medicínska služba sa určí podľa prílohy č. 12 alebo č. 13.",
                    "D - Označenie pre spôsob určenia medicínskej služby, kedy sa medicínska služba pre poistencov určí podľa hlavnej diagnózy podľa prílohy č. 14 alebo 15; ak hlavná diagnóza pre hospitalizáciu nebola určená poskytovateľom zdravotnej starostlivosti, za hlavnú diagnózu sa považuje diagnóza pri prepustení.",
                    "S - Označenie pre spôsob určenia medicínskej služby 'Identifikácia mŕtveho darcu orgánov' podľa prílohy č. 16,  ktorá sa môže vykonať spolu s medicínskymi službami určenými podľa spôsobu určenia podľa ostatných spôsobov určenia medicínskych služieb, medicínska služba sa určí podľa prílohy č. 16",
                    "M - Spôsob určenia medicínskych služieb spadajúcich do programu č. 98 - v hospitalizačných prípadoch, v ktorých bol vykázaný marker zo zoznamu markerov v prílohe č. 17, medicínska služba sa určí podľa prílohy č. 17.",
                    "Medicínska služba S99-99 nemá spôsob určenia medicínskej služby, do tejto medicínskej služby budú zaradené hospitalizačné prípady, ktoré neboli zaradené podľa vyššie uvedených spôsobom určenia medicínskej služby",
                ],
            },
            {
                "title": "Povinnosť medicínskej služby:",
                "subtitle": "Povinnosť medicínskej služby sa stanovuje pre najvyššiu úroveň povinného programu alebo najvyššiu úroveň prideleného doplnkového programu alebo najvyššiu úroveň nepovinného programu. V prípade, že je úroveň nemocnice vyššia ako úroveň programu, povinnosť sa stanovuje podľa úrovne nemocnice.",
            },
            {
                "title": "Označenie medicínskej služby:",
                "rows": ["1. P – povinná medicínska služba", "2. N – nepovinná medicínska služba"],
            },
            {
                "title": "Symboly pri minimálnych počtoch medicínskych služieb:",
                "rows": [
                    "Minimálny počet výkonov sa sčítava za všetky medicínske služby takto označené.",
                    "Minimálny počet výkonov sa sčítava za všetky medicínske služby takto označené.",
                    "Minimálny počet výkonov sa sčítava za všetky medicínske služby takto označené.",
                    "30 % pacientov s nervovými ochoreniami rôznej etiológie.",
                    "25 % pacientov s nervovými ochoreniami rôznej etiológie.",
                    "20 % pacientov s nervovými ochoreniami rôznej etiológie.",
                    "Minimálny počet výkonov sa sčítava za všetky medicínske služby takto označené.",
                    "Minimálny počet výkonov sa sčítava za všetky medicínske služby takto označené.",
                    "Minimálny počet výkonov sa sčítava za všetky medicínske služby takto označené.",
                ],
            },
            {
                "title": "Symboly pri čakacích lehotách:",
                "subtitle": "Čakacia doba 10 dní sa týka iba novodiagnostikovaných pacientov",
            },
            {
                "title": "Iné skratky:",
                "rows": [
                    "ASA - skóre pre posúdenie anesteziologického rizika podľa American Society of Anaesthesiology",
                    "AV Shunt - Artério-venózny shunt",
                    "BEVAR - z anglického branched endovascular aneurysm repair - nemá preklad",
                    "BSL - úroveň biologickéj bezpečnosti",
                    "C1 - C7 - stavce krčnej chrbtice",
                    "CML - chronická myeloidná leukémia",
                    "CMP - cievna mozgová príhoda",
                    "CNS - centrálna nervová sústava",
                    "CT - výpočtová tomografia",
                    "DBS - hĺbková mozgová stimulácia",
                    "DDC - dolné dýchacie cesty",
                    "DM - diabetes mellitus",
                    "EEG - elektroencefalografia",
                    "EKG - elektrokardiografia",
                    "EUG - extrauterinná gravidita",
                    "FEVAR - z anglického fenestrated endovascular aneurysm repair - nemá preklad",
                    "GERD - gastroezofageálna refluxová choroba",
                    "GIT - gastrointestinálny trakt",
                    "HIV - vírus ľudskej imunitnej nedostatočnosti",
                    "HRCT - výčtová tomografia s vysokým priestorovým rozlíšením",
                    "HSK - hysteroskopia",
                    "CHEVAR - z anglického chimmey endovascular aneurysm repair - nemá preklad",
                    "CHOCHP - chronická choroba pľúcna",
                    "KP - koniec panvový",
                    "L1 - L5 - stavce driekovej chrbtice",
                    "LU - lymfatická uzlina",
                    "MDS - myelodysplastický syndróm",
                    "MPN - myeloproliferatívne neoplázie",
                    "NCMP - náhla cievna mozgová porucha",
                    "NHL - non Hodgkinov lymfóm",
                    "NS - nervová sústava",
                    "OP výkon - operačný výkon",
                    "ORL - otorinolaryngológia",
                    "PFAPA syndróm - syndróm periodickej horúčky",
                    "Ph negatívne MP - Ph-negatívne myeloproliferatívne neoplázie",
                    "PKI - perkutánna koronárna intervencia",
                    "pPKI - primárna perkutánna koronárna intervencia",
                    "S1 - S5 - stavce krížovej chrbtice",
                    "T1 - T12 - stavce hrudnej chrbtice",
                    "TBC - tuberkulóza",
                    "UPV - umelá pľúcna ventilácia",
                    "VAD - z anglického ventricular assist devices - mechanické podporné systémy srdca",
                    "VVCH - vrodené vývojové chyby",
                ],
            },
        ],
    }

    P3 = {
        "file": "03_Personalne zabezpecenie materialno technicke vybavenie a dalsie poziadavky na jednotlive urovne.docx",
        "index": "3",
    }

    P4 = {"file": "04_Indikatory kvality pre ustavnu starostlivost.xlsx", "index": "4"}

    P5 = {
        "columns": ["drg", "doplnujuce_kriterium", "kod_ms", "nazov_ms"],
        "file": "05_Sposob urcenia medicinskej sluzby pre novorodencov_NOV.xlsx",
        "index": "5",
    }

    P6 = {
        "columns": ["drg", "doplnujuce_kriterium", "kod_ms", "nazov_ms"],
        "file": "06_Sposob urcenia medicinskej sluzby podla skupiny klasifikacneho systemu a diagnozy_DRGD.xlsx",
        "index": "6",
    }

    P7 = {
        "columns": ["kod_vykonu", "nazov_vykonu", "nazov_ms", "kod_ms"],
        "file": "07_Sposob urcenia medicinskej sluzby podla hlavneho ZV a zdravotneho vykonu pre deti_VV.xlsx",
        "index": "7",
    }

    P7a = {
        "columns": ["kod_vykonu", "nazov_vykonu", "nazov_ms", "kod_ms"],
        "file": "07a_Sposob urcenia medicinskej sluzby podla markera a zdravotneho vykonu pre deti MV.xlsx",
        "index": "7a",
    }

    P8 = {
        "columns": ["kod_vykonu", "nazov_vykonu", "nazov_ms", "kod_ms"],
        "file": "08_Sposob urcenia medicinskej sluzby podla hlavneho ZV a ZV pre dospelych VV.xlsx",
        "index": "8",
    }

    P8a = {
        "columns": ["kod_vykonu", "nazov_vykonu", "nazov_ms", "kod_ms"],
        "file": "08a_Sposob urcenia medicinskej sluzby podla markera a ZV pre dospelych MV.xlsx",
        "index": "8a",
    }

    P9 = {
        "columns": [
            "kod_hlavneho_vykonu",
            "nazov_hlavneho_vykonu",
            "skupina_diagnoz",
            "kod_ms",
            "nazov_ms",
        ],
        "file": "09_Sposob urcenie medicinskej sluzby podla hlavneho vykonu a diagnozy_VD.xlsx",
        "index": "9",
    }

    P9a = {
        "columns": [
            "kod_markera",
            "nazov_markera",
            "skupina_diagnoz",
            "kod_hlavnej_diagnozy",
            "nazov_hlavnej_diagnozy",
        ],
        "file": "09a_Sposob urcenie medicinskej sluzby podla markera a diagnozy_MD.xlsx",
        "index": "9a",
    }

    P10 = {
        "columns": [
            "skupina_diagnoz",
            "kod_hlavnej_diagnozy",
            "nazov_hlavnej_diagnozy",
            "kod_ms",
            "nazov_ms",
        ],
        "file": "10_Sposob urcenia medicinskej sluzby podla hlavnej a vedlajsej diagnozy_DD.xlsx",
        "index": "10",
    }

    P12 = {
        "columns": ["kod_vykonu", "nazov_vykonu", "kod_ms", "nazov_ms"],
        "columns_full": [
            "Kód výkonu",
            "Zdravotný výkon",
            "Kód medicínskej služby",
            "Medicínska služba",
        ],
        "column_widths": {"A": 14.71, "B": 49.71, "C": 19.71, "D": 50.14, "E": 30},
        "description": "Ak bol poistencovi vo veku 18 rokov a menej poskytnutý hlavný zdravotný výkon podľa stĺpca 'zdravotný výkon', hospitalizácii sa určí medicínska služba podľa stĺpca 'medicínska služba' [V].",
        "diff_translations": {
            "added": "Pridanie výkonu",
            "removed": "Odstránené zaradenie výkonu",
            "edited": "Nové zaradenie výkonu",
            "original": "Pôvodné zaradenie výkonu",
            "same": "",
        },
        "file": "12_Sposob urcenia medicinskej sluzby podla hlavneho vykonu pre deti_V.xlsx",
        "headers": ["Príloha č. 12", "k vyhláške č. .../... Z. z."],
        "index": "12",
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
        "vysvetlivky": [
            {
                "title": "Vysvetlivky skratiek:",
                "rows": [
                    "AV Shunt - Artério-venózny shunt",
                    "BEVAR - z anglického branched endovascular aneurysm repair - nemá preklad",
                    "CMP - cievna mozgová príhoda",
                    "CT - výpočtová tomografia",
                    "DBS - hĺbková mozgová stimulácia",
                    "EEG - elektroencefalografia",
                    "EKG - elektrokardiografia",
                    "EUG - extrauterinná gravidita",
                    "FEVAR - z anglického fenestrated endovascular aneurysm repair - nemá preklad",
                    "GERD - gastroezofageálna refluxová choroba",
                    "HRCT - výčtová tomografia s vysokým priestorovým rozlíšením",
                    "HSK - hysteroskopia",
                    "CHEVAR - z anglického chimmey endovascular aneurysm repair - nemá preklad",
                    "KP - koniec panvový",
                    "LU - lymfatická uzlina",
                    "MR - magnetická rezonancia",
                    "ORL - otorinolaryngológia",
                    "PKI - perkutánna koronárna intervencia",
                    "pPKI - primárna perkutánna koronárna intervencia",
                    "VAD - z anglického ventricular assist devices - mechanické podporné systémy srdca",
                    "VVCH - vrodené vývojové chyby",
                ],
            },
            {
                "title": "Vysvetlivky:",
                "rows": [
                    "V - Označenie pre spôsob určenia medicínskej služby, kedy bol poistencovi počas hospitalizácie poskytnutý hlavný zdravotný výkon zo zoznamu v prílohe č.13 alebo č. 14, medicínska služba sa určí podľa prílohy č. 13 alebo č. 14.",
                ],
            },
        ],
    }

    P13 = {
        **P12,
        "description": "Ak bol poistencovi vo veku viac ako 18 rokov poskytnutý hlavný zdraovotný výkon podľa stĺpca 'zdravotný výkon', hospitalizácii sa určí medicínska služba podľa stĺpca 'medicínska služba' [V].",
        "file": "13_Sposob urcenia medicinskej sluzby podla hlavneho vykonu pre dospelych_V.xlsx",
        "headers": ["Príloha č. 13", "k vyhláške č. .../... Z. z."],
        "index": "13",
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
        "columns": ["kod_diagnozy", "nazov_diagnozy", "kod_ms", "nazov_ms"],
        "columns_full": [
            "Kód diagnózy",
            "Hlavná diagnóza",
            "Kód medicínskej služby",
            "Medicínska služba",
        ],
        "column_widths": {"A": 14.71, "B": 49.71, "C": 19.71, "D": 50.14, "E": 30},
        "description": "Ak bola poistencov vo veku 18 rokov a menej pri hospitalizácii vykázaná hlavná diagnóza podľa stĺpca 'hlavná diagnóza', hospitalizácii sa určí medicínska služba podľa stĺpca 'medicínska služba' [D].",
        "diff_translations": {
            "added": "Pridanie diagnózy",
            "removed": "Odstránenie diagnózy",
            "edited": "Nové zaradenie diagnózy",
            "original": "Pôvodné zaradenie diagnózy",
            "same": "",
        },
        "file": "14_Sposob urcenia medicinskej sluzby podla hlavnej diagnozy pre deti_D.xlsx",
        "headers": ["Príloha č. 14", "k vyhláške č. .../... Z. z."],
        "index": "14",
        "title": "Spôsob určenia medicínskej služby podľa hlavnej diagnózy pre poistencov vo veku 18 rokov a menej",
        "vysvetlivky": [
            {
                "title": "Vysvetlivky skratiek:",
                "rows": [
                    "AIM - anestéziológia a intenzívna medicína",
                    "CNS - centrálna nervová sústava",
                    "GIT - gastrointestinálny trakt",
                    "NCMP - náhla cievna mozgová príhoda",
                ],
            },
            {
                "title": "Vysvetlivky:",
                "rows": [
                    "D - Označenie pre spôsob určenia medicínskej služby, kedy sa medicínska služba pre poistencov určí podľa hlavnej diagnózy podľa prílohy č. 14 alebo č. 15; ak hlavná diagnóza pre hospitalizáciu nebola určená poskytovateľom zdravotnej starostlivosti, za hlavnú diagnózu sa považuje diagnóza pri prepustení.",
                ],
            },
        ],
    }

    P15 = {
        **P14,
        "description": "Ak bola poistencovi vo veku viac ako 18 rokov pri hospitalizácii vykázaná hlavná diagnóza podľa stĺpca 'hlavná diagnóza', hospitalizácii sa určí medicínska služba podľa stĺpca 'medicínska služba' [D].",
        "file": "15_Sposob urcenia medicinskej sluzby podla hlavnej diagnozy pre dospelych_D.xlsx",
        "headers": ["Príloha č. 15", "k vyhláške č. .../... Z. z."],
        "index": "15",
        "title": "Spôsob určenia medicínskej služby podľa hlavnej diagnózy pre poistencov vo veku viac ako 18 rokov",
    }

    P16 = {
        "columns": ["kod_diagnozy", "nazov_diagnozy"],
        "file": "16_Sposob urcenia medicinskej sluzby podla specialnych pravidiel_S.xlsx",
        "index": "16",
    }

    P17 = {
        "columns": ["kod_markera", "nazov_markera", "kod_ms", "nazov_ms"],
        "file": "17_Sposob urcenia medicinskej sluzby pre program 98.xlsx",
        "index": "17",
    }


class PrilohyXlsxFormats:
    """Metadata related to generated XLSX files"""

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
