import configparser

cfg: configparser.ConfigParser = configparser.ConfigParser()
cfg.read("config.cfg")

CARDS_DIR: str = cfg['Paths']["data_dir"]
