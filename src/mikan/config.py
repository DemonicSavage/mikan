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
from pathlib import Path


class Config:
    def __init__(self, path: Path):
        self._cfg_parser = configparser.ConfigParser()
        self._cfg_file = path / "config.cfg"

        try:
            if not self._cfg_file.exists():
                self._create_initial_config()

            self._cfg_parser.read(self._cfg_file)

            self.data_dir = Path(self._cfg_parser.get("Paths", "data_dir"))
            self.cookie = self._cfg_parser.get("Other", "cookie", fallback="")
            self.max_conn = self._cfg_parser.getint("Other", "max_connections", fallback=10)
        except (configparser.Error, ValueError) as e:
            print(f"Error occurred while reading the configuration file: {e}")

    def _create_initial_config(self) -> None:
        self._cfg_parser["Paths"] = {}

        try:
            selected_dir = input(
                "Please enter the directory cards should be downloaded to (leave empty to default to ~/Idol_Cards): "
            )
            selected_dir = selected_dir.strip() or "~/Idol_Cards"

            self._cfg_parser["Paths"]["data_dir"] = str(Path(selected_dir).expanduser().resolve())
            with open(self._cfg_file, "w") as file:
                self._cfg_parser.write(file)
        except (configparser.Error, ValueError) as e:
            print(f"Error occurred while creating the initial configuration: {e}")
