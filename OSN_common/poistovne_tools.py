import pandas as pd

from OSN_common.helpers import load_json, DATA_PATH


LOAD_CSV_ARGS = load_json('poistovne_loading_args.json')
POISTOVNE = load_json('poistovne.json')


def load_data_zp(rok, zoznam_zp):
    data = {}
    for kod in zoznam_zp:
        print(f'Nacitavam data pre poistovnu {POISTOVNE[kod]["nazov"]}')

        datove_subory = (
            DATA_PATH / "06_Dáta od zdravotných poisťovní" / str(rok) / str(kod)
        )

        data[kod] = {}

        for data_name, data_structure in POISTOVNE[kod]["subory"][rok].items():
            data[kod][data_name] = pd.DataFrame()

            for _i in range(len(data_structure["nazvy_suborov"])):

                nazov_suboru = data_structure["nazvy_suborov"][_i]
                argumenty = (
                    LOAD_CSV_ARGS[data_name]
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