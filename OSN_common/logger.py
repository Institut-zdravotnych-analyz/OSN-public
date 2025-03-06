import colorlog
import logging
from pathlib import Path
import sys

from OSN_common.constants import LOG_COLOR_SCHEME, LOG_FMT_FILE, LOG_FMT_CONSOLE


class ColorLogger:
    """
    Custom colorful logger:
        - streaming output to stdout + logfile (compatible with jupyter notebooks)
        - custom formatting [message, date]
        - colorizing logs
    """

    NAME_2_LEVEL = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    def __init__(self, log_file: Path | str = None, log_level: str = 'debug'):
        """
        Initialize logger with custom formatting and color scheme.
        if `log_file` is not provided, logger streams only to console.
        """

        self.log_file = log_file
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.NAME_2_LEVEL[log_level])
        self.logger.propagate = False

        # prevents logger to stack in Jupyter console when ran multiple times
        while self.logger.hasHandlers():
            self.logger.handlers[0].close
            self.logger.removeHandler(self.logger.handlers[0])

        # logging to console
        formatter = colorlog.ColoredFormatter(
            fmt=LOG_FMT_CONSOLE,
            datefmt='%H:%M:%S',
            reset=True,
            log_colors=LOG_COLOR_SCHEME
        )
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # optional logging to file
        if log_file:
            formatter = logging.Formatter(
                fmt=LOG_FMT_FILE,
                datefmt='%Y-%m-%d %H:%M:%S',
            )
            handler = logging.FileHandler(filename=log_file, mode="w")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            print(f'Initialised logfile at: {log_file}')

    def debug(self, msg: str):
        self.logger.debug(msg)

    def info(self, msg: str):
        self.logger.info(msg)
    
    def warning(self, msg: str):
        self.logger.warning(msg)
    
    def error(self, msg: str):
        self.logger.error(msg)
    
    def critical(self, msg: str):
        self.logger.critical(msg)

logger = ColorLogger()
