import os
from pathlib import Path
from typing import List
from unicodedata import normalize

from OSN_common.logger import logger


def check_path_existence(paths: Path | List[Path]) -> None:
    for p in paths:
        if not p.exists():
            logger.warning(f'Path does not exist! {p}')
            return
    logger.info('✅ All paths exist')


def norm_path(p: Path) -> Path:
    """
    Normalize path so that e.g. accentation is consistent between OS (e.g. "š" between MacOS and Windows)
    """
    return Path(normalize('NFC', str(p)))

OSN_PATH = os.environ.get('OSN_data')
if OSN_PATH is None:
    raise ValueError("Environmental variable 'OSN_data' is not set. Please follow instructions in README.md in order to continue")

OSN_PATH = norm_path(Path(OSN_PATH).expanduser())
if not OSN_PATH.exists():
    raise ValueError(f"Path OSN_data={OSN_PATH} does not exist! Check manually the exported path and try again.")

DATA_PATH = norm_path(OSN_PATH / '11_Dátové súbory a prevodníky')
if not DATA_PATH.exists():
    raise ValueError(f"Path DATA_PATH={DATA_PATH} does not exist! Check manually the exported path and try again.")

KATEGORIZACIA_PATH = norm_path(OSN_PATH / '03_Kategorizácia ÚZS' / '01_Riadna kategorizacia' / '07_Kategorizácia ÚZS 2025')
