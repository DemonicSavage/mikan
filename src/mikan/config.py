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
import os
from pathlib import Path

import platformdirs

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
cfg = configparser.ConfigParser()

cfg_dir = Path(platformdirs.user_config_dir("mikan", ensure_exists=True))
cfg_file = cfg_dir / "config.cfg"


def get_data_dir() -> Path:
    if not cfg_file.exists():
        cfg["Paths"] = {}

        selected_dir = input(
            """Please enter the directory cards should be downloaded \
to (leave empty to default to ~/Idol_Cards): """
        )
        if selected_dir.strip() == "":
            selected_dir = "~/Idol_Cards"

        cfg["Paths"]["data_dir"] = str(Path(selected_dir).expanduser().resolve())
        with open(cfg_file, "w") as file:
            cfg.write(file)

    cfg.read(cfg_file)
    return Path(cfg["Paths"]["data_dir"])
