from OSN_common.constants import POISTIVNE_ARGS, POISTOVNE
from collections import defaultdict

import pandas as pd


def load_data_zp(data_folder_path, rok, zoznam_zp):
    data = {}
    for kod in zoznam_zp:
        print(f'Nacitavam data pre poistovnu {POISTOVNE[kod]["nazov"]}')

        datove_subory = data_folder_path / str(rok) / str(kod)

        data[kod] = {}

        for data_name, data_structure in POISTOVNE[kod]["subory"][rok].items():
            data[kod][data_name] = pd.DataFrame()

            for _i in range(len(data_structure["nazvy_suborov"])):

                nazov_suboru = data_structure["nazvy_suborov"][_i]
                argumenty = POISTIVNE_ARGS[data_name] | data_structure["argumenty"][_i]

                print(f"Nacitavam data zo suboru {nazov_suboru}")
                df = pd.read_csv(datove_subory / nazov_suboru, **argumenty)

                stripped = df.select_dtypes(include="object").apply(lambda col: col.str.strip()).replace("", pd.NA)
                df.loc[:, stripped.columns] = stripped

                if "kod_zp" not in df.columns:
                    df.insert(0, "kod_zp", kod)

                data[kod][data_name] = pd.concat([data[kod][data_name], df], ignore_index=True)

    return data


def load_zoznam_obci(path):
    return pd.read_excel(
        path,
        dtype=defaultdict(
            lambda: "str",
            {"Počet obyvateľov 2021": "Int64"},
        ),
    )


def load_psc_2_zuj(path):
    return pd.read_csv(path, sep=";", dtype=defaultdict(lambda: "str", {"ZUJ_pravdepodobnost": "float"}))


def load_pzs_12(path):
    return pd.read_csv(path, sep=";", dtype=defaultdict(lambda: "str"))
