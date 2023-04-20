# Copyright (C) 2022-2023 DemonicSavage
# This file is part of SIFAS Card Downloader.

# SIFAS Card Downloader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.

# SIFAS Card Downloader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License

import configparser
from pathlib import Path

cfg = configparser.ConfigParser()
cfg.read("config.cfg")

CARDS_DIR = Path(cfg["Paths"]["data_dir"])
