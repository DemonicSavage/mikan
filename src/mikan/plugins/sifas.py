#!/usr/bin/env python3
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

from mikan.plugins.default import DefaultPlugin
from mikan.plugins.sif2 import SIF2


class SIFAS(SIF2, DefaultPlugin):
    card_dir = "SIFAS_Cards"
    url = "https://idol.st/ajax/allstars/card/"
    list_url = "https://idol.st/ajax/allstars/cards/?page="
    cli_arg = "sifas"
    desc = "SIFAS cards"
