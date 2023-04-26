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

from dataclasses import dataclass
from typing import ClassVar, TypeAlias


@dataclass
class Card:
    results_dir: ClassVar = "SIFAS_Cards"
    list_url_template: ClassVar = "https://idol.st/ajax/allstars/cards/?page="
    url_template: ClassVar = "https://idol.st/ajax/allstars/card/"


@dataclass
class Still:
    results_dir: ClassVar = "SIFAS_Stills"
    list_url_template: ClassVar = "https://idol.st/ajax/allstars/stills/?page="
    url_template: ClassVar = "https://idol.st/ajax/allstars/still/"


@dataclass
class SIFCard:
    results_dir: ClassVar = "SIF_Cards"
    list_url_template: ClassVar = "https://schoolido.lu/api/cardids/"
    url_template: ClassVar = "https://schoolido.lu/api/cards/"


Item: TypeAlias = Card | Still | SIFCard
