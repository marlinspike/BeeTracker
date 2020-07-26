import logging
import sys
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = "my_app.log"
_Logger = None

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler


def get_file_handler():
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler


def get_logger(logger_name=__name__) -> logging.Logger:
   global _Logger
   if(_Logger == None):
      _Logger = logging.getLogger(logger_name)
      # better to have too much log than not enough
      _Logger.setLevel(logging.DEBUG)
      _Logger.addHandler(get_console_handler())
      _Logger.addHandler(get_file_handler())
      # with this pattern, it's rarely necessary to propagate the error up to parent
      _Logger.propagate = False

   return _Logger
