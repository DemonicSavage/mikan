import configparser
from pathlib import Path

cfg = configparser.ConfigParser()
cfg.read("config.cfg")

CARDS_DIR = Path(cfg["Paths"]["data_dir"])
