import re
from pandas import notna
from pathlib import Path
import os


def zjednot_kod(kod):
    return re.sub("[^0-9a-zA-Z]", "", kod).lower() if notna(kod) else kod


def ziskaj_data_path():
    if data_path := os.environ.get("OSN_data"):
        return Path(data_path)
    else:
        raise ValueError(
            'V environmentalnej premennej "OSN_data" sa nenachadza cesta k datam.'
        )
