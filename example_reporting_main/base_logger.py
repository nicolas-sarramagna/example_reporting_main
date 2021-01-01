import logging
from logging.config import fileConfig
import os
from os import path

# init logging

# for circleci which do not support volumes
config_folder = os.getenv("config_folder", "config")

log_file_path = path.join(path.dirname(path.abspath(__file__)), config_folder + "/logging.cfg")
fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)
