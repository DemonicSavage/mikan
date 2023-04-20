# Copyright (C) 2022-2023 DemonicSavage
# This file is part of Mikan.

# Mikan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.

# Mikan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License

import configparser
import shutil
from pathlib import Path

import platformdirs

cfg = configparser.ConfigParser()

cfg_dir = Path(platformdirs.user_config_dir("mikan", ensure_exists=True))
cfg_file = cfg_dir / "config.cfg"

if not cfg_file.exists():
    shutil.copy("default_config.cfg", cfg_file)

cfg.read(cfg_dir / "config.cfg")

CARDS_DIR = Path(cfg["Paths"]["data_dir"])
