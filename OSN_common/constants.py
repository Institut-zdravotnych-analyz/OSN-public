### LOGER

LOG_COLOR_SCHEME = {
    'DEBUG':    'cyan',
    'INFO':     'green',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'white,bg_red',
}

LOG_FMT_FILE = "%(asctime)s %(levelname)8s -- %(message)s"
LOG_FMT_CONSOLE = "%(log_color)s%(asctime)s %(levelname)8s -- %(reset)s%(white)s%(message)s"

### CONVERTERS

INT_2_ROMAN = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V'}
ROMAN_2_INT = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5}

### PRILOHY

P1_MAIN_COLS = [
    'cislo_programu',
    'nazov_programu',
    'uroven_programu'
]

P1_POVINNOSTI_P_COLS = [
    'povinnost_programu_V',
    'povinnost_programu_IV',
    'povinnost_programu_III',
    'povinnost_programu_II',
    'povinnost_programu_I',
]

P1_DATE_COLS = ['od', 'do']

P1_XLSX = {
    'columns': P1_MAIN_COLS + P1_POVINNOSTI_P_COLS + P1_DATE_COLS,
    'file': '01_Programovy profil.xlsx'
}

P2_MAIN_COLS = [
    'cislo_programu',
    'kod_ms',
    'zdielana_ms',
    'nazov_ms', 
    'sposob_urcenia'
]

P2_UROVNE_COLS = [
    'uroven_ms_dospeli', 
    'uroven_ms_deti_0', 
    'uroven_ms_deti_1', 
    'uroven_ms_deti_7', 
    'uroven_ms_deti_16'
]

P2_POVINNOSTI_MS_COLS = [
    'povinnost_ms_V',
    'povinnost_ms_IV',
    'povinnost_ms_III',
    'povinnost_ms_II',
    'povinnost_ms_I',
]

P2_NUM_COLS = [
    'casova_dostupnost', 
    'minimum_na_nemocnicu', 
    'minimum_na_lekara'
]

P2_XLSX = {
    'columns': P2_MAIN_COLS + P2_UROVNE_COLS + P2_POVINNOSTI_MS_COLS + P2_NUM_COLS,
    'columns_full': [
        'Číslo programu',
        'Kód medicínskej služby',
        'Zdieľaná medicínska služba',
        'Názov medicínskej služby',
        'Spôsob určenia',
        'Uroveň dospelí',
        'Uroveň deti do 1r',
        'Uroveň deti 1-6r',
        'Uroveň deti 7-15r',
        'Uroveň deti 16-18r',
        'Povinnosť V.',
        'Povinnosť IV.',
        'Povinnosť III.',
        'Povinnosť II.',
        'Povinnosť I.',
        'Časová dostupnosť',
        'Minimum na nemocnicu',
        'Minimum na lekára'
    ],
    'column_widths': {
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
    'description': '',
    'diff_translations': {
        'added': 'Nová MS',
        'removed': 'Odstránená MS',
        'edited': 'Upravená MS',
        'same': ''
    },
    'file': '02_Zoznam-medicinskych-sluzieb.xlsx',
    'title': "Zoznam medicínskych služieb so zaradením do programov a podmienky pre poskytnutie medicínskych služieb v nemocnici"
}

P3_XLSX = {
    'file': '03_Personalne zabezpecenie materialno technicke vybavenie a dalsie poziadavky na jednotlive urovne.docx'
}

P4_XLSX = {
    'file': '04_Indikatory kvality pre ustavnu starostlivost.xlsx'
}

P5_XLSX = {
    'file': '05_Sposob urcenia medicinskej sluzby pre novorodencov_NOV.xlsx'
}

P6_XLSX = {
    'file': '06_Sposob urcenia medicinskej sluzby podla skupiny klasifikacneho systemu a diagnozy_DRGD.xlsx'
}

P7_XLSX = {
    'columns': ['kod_vykonu', 'nazov_vykonu', 'nazov_ms', 'kod_ms'],
    'file': '07_Sposob urcenia medicinskej sluzby podla hlavneho zdravotneho vykonu a zdravotneho vykonu pre deti_VV.xlsx'
}

P8_XLSX = {
    'file': '08_Sposob urcenia medicinskej sluzby podla hlavnho zdravotnho vykonu a zdravotneho vykonu pre dospelych_VV.xlsx'
}

P9_XLSX = {
    'columns': ['kod_hlavneho_vykonu', 'nazov_hlavneho_vykonu', 'skupina_diagnoz', 'kod_ms', 'nazov_ms'],
    'file': '09_Sposob urcenie medicinskej sluzby podla hlavneho vykonu a diagnozy_VD.xlsx'
}

P10_XLSX = {
    'columns': ['skupina_diagnoz', 'kod_hlavnej_diagnozy', 'nazov_hlavnej_diagnozy', 'kod_ms', 'nazov_ms'],
    'file': '10_Sposob urcenia medicinskej sluzby podla hlavnej a vedlajsej diagnozy_DD.xlsx'
}

P12_XLSX = {    
    'abbrvs': {
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
        "VVCH": "vrodené vývojové chyby"
    },
    'columns': ['kod_vykonu', 'nazov_vykonu', 'kod_ms', 'nazov_ms'],
    'columns_full': ['Kód výkonu', 'Zdravotný výkon', 'Kód medicínskej služby', 'Medicínska služba', 'Typ zmeny'],
    'column_widths': {
        "A": 14.71,
        "B": 49.71,
        "C": 19.71,
        "D": 50.14,
        "E": 30
    },
    'description': "Ak bol poistencovi vo veku 18 rokov a menej poskytnutý hlavný zdravotný výkon podľa stĺpca \"zdravotný výkon\", hospitalizácii sa určí medicínska služba podľa stĺpca \"medicínska služba\" (V).",
    'diff_translations': {
        'added': 'Nové zaradenie výkonu',
        'removed': 'Odstránené zaradenie výkonu',
        'edited': 'Upravené zaradenie výkonu',
        'same': ''
    },
    'file': '12_Sposob urcenia medicinskej sluzby podla hlavneho vykonu pre deti_V.xlsx',
    'footer': {
        'V': "Označenie pre spôsob určenia medicínskej služby, kedy bol poistencovi počas hospitalizácie poskytnutý hlavný zdravotný výkon zo zoznamu v prílohe č.13 alebo č. 14, medicínska služba sa určí podľa prílohy č. 13 alebo č. 14."
    },
    'title': "Spôsob určenia medicínskej služby podľa hlavného výkonu pre poistencov vo veku 18 rokov a menej"
}

P13_XLSX = {
    **P12_XLSX,
    'description': "Ak bol poistencovi vo veku viac ako 18 rokov poskytnutý hlavný zdraovotný výkon podľa stĺpca \"zdravotný výkon\", hospitalizácii sa určí medicínska služba podľa stĺpca \"medicínska služba\" (V).",
    'file': '13_Sposob urcenia medicinskej sluzby podla hlavneho vykonu pre dospelych_V.xlsx',
    'title': "Spôsob určenia medicínskej služby podľa hlavného výkonu pre poistencov vo veku viac ako 18 rokov"
}

P14_XLSX = {
    'abbrvs': {
        "AIM": "anestéziológia a intenzívna medicína",
        "CNS": "centrálna nervová sústava",
        "GIT": "gastrointestinálny trakt",
        "NCMP": "náhla cievna mozgová príhoda"
    },
    'columns': ['kod_diagnozy', 'nazov_diagnozy', 'kod_ms', 'nazov_ms'],
    'columns_full': ['Kód diagnózy', 'Hlavná diagnóza', 'Kód medicínskej služby', 'Medicínska služba', 'Typ zmeny'],
    'column_widths': {
        "A": 14.71,
        "B": 49.71,
        "C": 19.71,
        "D": 50.14,
        "E": 30
    },
    'description': "Ak bola poistencov vo veku 18 rokov a menej pri hospitalizácii vykázaná hlavná diagnóza podľa stĺpca \"hlavná diagnóza\", hospitalizácii sa určí medicínska služba podľa stĺpca \"medicínska služba\" (D).",
    'diff_translations': {
        'added': 'Nová diagnóza',
        'removed': 'Odstránenie diagnózy',
        'edited': 'Preradenie diagnózy',
        'same': ''
    },
    'file': '14_Sposob urcenia medicinskej sluzby podla hlavnej diagnozy pre deti_D.xlsx',
    'footer': {
        'D': "Označenie pre spôsob určenia medicínskej služby, kedy sa medicínska služba pre poistencov určí podľa hlavnej diagnózy podľa prílohy č. 14 alebo č. 15; ak hlavná diagnóza pre hospitalizáciu nebola určená poskytovateľom zdravotnej starostlivosti, za hlavnú diagnózu sa považuje diagnóza pri prepustení."
    },
    'title': "Spôsob určenia medicínskej služby podľa hlavnej diagnózy pre poistencov vo veku 18 rokov a menej"
}

P15_XLSX = {
    **P14_XLSX,
    'description': "Ak bola poistencovi vo veku viac ako 18 rokov pri hospitalizácii vykázaná hlavná diagnóza podľa stĺpca \"hlavná diagnóza\", hospitalizácii sa určí medicínska služba podľa stĺpca \"medicínska služba\" (D).",
    'file': '15_Sposob urcenia medicinskej sluzby podla hlavnej diagnozy pre dospelych_D.xlsx',
    'title': "Spôsob určenia medicínskej služby podľa hlavnej diagnózy pre poistencov vo veku viac ako 18 rokov"
}

P16_XLSX = {
    'file': '16_Sposob urcenia medicinskej sluzby podla specialnych pravidiel_S.xlsx'
}

P17_XLSX = {
    'file': '17_Sposob urcenia medicinskej sluzby pre program 98.xlsx'
}
