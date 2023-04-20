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

import re
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, TypeAlias


@dataclass
class Card:
    results_dir: ClassVar = "SIFAS_Cards"
    list_url_template: ClassVar = "https://idol.st/ajax/allstars/cards/?page="
    url_template: ClassVar = "https://idol.st/ajax/allstars/card/"
    json_filename: ClassVar = "sifas_cards.json"

    key: int
    idol: str
    rarity: str
    attribute: str
    unit: str
    subunit: str
    year: str
    normal_url: str
    idolized_url: str

    def is_double_sized(self) -> bool:
        pattern = re.compile(r"/2x/")
        return pattern.search(self.normal_url) is not None

    def get_urls(self) -> list[str]:
        return [self.normal_url, self.idolized_url]

    def set_url(self, i: int, url: str) -> None:
        if i == 0:
            self.normal_url = url
        else:
            self.idolized_url = url

    def needs_update(self) -> bool:
        return not self.is_double_sized() and self.rarity != "Rare"

    def get_paths(self, path: Path) -> list[Path]:
        file_name = f"{self.key}_{self.unit}_{self.idol}"
        base_path = path / self.results_dir

        normal_path = f"{file_name}_Normal{Path(self.normal_url).suffix}"
        idolized_path = normal_path.replace("Normal", "Idolized")

        return [base_path / normal_path, base_path / idolized_path]


@dataclass
class Still:
    results_dir: ClassVar = "SIFAS_Stills"
    list_url_template: ClassVar = "https://idol.st/ajax/allstars/stills/?page="
    url_template: ClassVar = "https://idol.st/ajax/allstars/still/"
    json_filename: ClassVar = "sifas_stills.json"

    key: int
    url: str

    def is_double_sized(self) -> bool:
        pattern = re.compile(r"/2x/")
        return pattern.search(self.url) is not None

    def get_urls(self) -> list[str]:
        return [self.url]

    def set_url(self, _: int, url: str) -> None:
        self.url = url

    def needs_update(self) -> bool:
        return not self.is_double_sized()

    def get_paths(self, path: Path) -> list[Path]:
        file_name = f"{self.key}_Still"
        base_path = path / self.results_dir

        return [base_path / f"{file_name}{Path(self.url).suffix}"]


@dataclass
class SIFCard:
    results_dir: ClassVar = "SIF_Cards"
    list_url_template: ClassVar = ""
    url_template: ClassVar = ""
    json_filename: ClassVar = "sif_cards.json"

    key: int
    idol: str
    rarity: str
    attribute: str
    unit: str
    subunit: str
    year: str
    normal_url: str
    idolized_url: str

    def is_double_sized(self) -> bool:
        pass

    def get_urls(self) -> list[str]:
        return [x for x in [self.normal_url, self.idolized_url] if x is not None]

    def set_url(self, i: int, url: str) -> None:
        pass

    def needs_update(self) -> bool:
        return False

    def get_paths(self, path: Path) -> list[Path]:
        file_name = f"{self.key}_{self.idol}"
        base_path = path / self.results_dir

        normal_path, idolized_path = None, None
        if self.normal_url:
            normal_path = f"{file_name}_Normal{Path(self.normal_url).suffix}"
        if self.idolized_url:
            idolized_path = f"{file_name}_Idolized{Path(self.idolized_url).suffix}"

        return [base_path / x for x in [normal_path, idolized_path] if x is not None]


Item: TypeAlias = Card | Still | SIFCard
