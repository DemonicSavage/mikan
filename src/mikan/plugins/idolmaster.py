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


class Idolmaster(SIF2, DefaultPlugin):
    card_dir = "Idolmaster_Cards"
    url = "https://cinderella.pro/ajax/card/"
    list_url = "https://cinderella.pro/ajax/cards/?page="
    cli_arg = "idolmaster"
    desc = "Idolmaster Cinderella Girls cards"

    @staticmethod
    def item_renamer_fn(url: str) -> str:  # pragma: no cover
        if "/a/" in url:
            name = url.split("/")[-1]
            stem = name.split(".")[-2]
            suffix = name.split(".")[-1]
            return f"{stem}_a.{suffix}"
        return url.split("/")[-1]

    class ItemParser:
        async def create_item(self, data: ClientResponse) -> list[str]:
            page = bs4.BeautifulSoup(await data.text(), features="lxml")

            items = page.find_all(class_="btn-sm")

            if not items:
                raise ParsingError("An error occured while getting a card.")

            urls = []
            for item in items:
                href = item.get("href")
                if "/art/" in href or "/art_hd/" in href:
                    urls.append(href)

            return urls
