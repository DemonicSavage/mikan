import configparser
from pathlib import Path

cfg: configparser.ConfigParser = configparser.ConfigParser()
cfg.read("config.cfg")

CARDS_DIR: Path = Path(cfg['Paths']["data_dir"])
