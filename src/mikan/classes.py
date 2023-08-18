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

from collections import namedtuple

CardType = namedtuple("CardType", ["results_dir", "list_url_template", "url_template"])

Card = CardType("SIFAS_Cards", "https://idol.st/ajax/allstars/cards/?page=", "https://idol.st/ajax/allstars/card/")
Still = CardType("SIFAS_Stills", "https://idol.st/ajax/allstars/stills/?page=", "https://idol.st/ajax/allstars/still/")
SIFCard = CardType("SIF_Cards", "https://schoolido.lu/api/cardids/", "https://schoolido.lu/api/cards/")
SIF2Card = CardType("SIF2_Cards", "https://idol.st/ajax/SIF2/cards/?page=", "https://idol.st/ajax/SIF2/card/")
