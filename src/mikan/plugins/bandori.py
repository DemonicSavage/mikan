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

import bs4
from aiohttp import ClientResponse

from mikan.html_parser import ParsingError
from mikan.plugins.default import DefaultPlugin
from mikan.plugins.sif2 import SIF2


class Bandori(SIF2, DefaultPlugin):
    card_dir = "Bandori_Cards"
    url = "https://bandori.party/ajax/card/"
    list_url = "https://bandori.party/ajax/cards/?page="
    cli_arg = "bandori"
    desc = "Bandori cards"

    class ItemParser:
        async def create_item(self, data: ClientResponse) -> list[str]:
            page = bs4.BeautifulSoup(await data.text(), features="lxml")

            if isinstance(top_item := page.find(attrs={"data-field": "arts"}), bs4.Tag):
                links = top_item.find_all("a")
                return [href for link in links if "/transparent/" not in (href := link.get("href"))]

            raise ParsingError("An error occured while getting a card.")
