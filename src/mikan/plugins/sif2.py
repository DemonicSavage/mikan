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

import re
from typing import Any

import bs4
from aiohttp import ClientResponse

from mikan.html_parser import ParsingError
from mikan.plugins.default import DefaultPlugin


class SIF2(DefaultPlugin):
    card_dir = "SIF2_Cards"
    url = "https://idol.st/ajax/SIF2/card/"
    list_url = "https://idol.st/ajax/SIF2/cards/?page="
    cli_arg = "sif2"
    desc = "SIF2 cards"

    class ListParser:
        async def get_page(self, data: Any) -> list[int]:
            nums: list[int] = []
            pattern = re.compile(r"/(\d+)/")

            page = bs4.BeautifulSoup(await data.text(), features="lxml")
            items = page.find_all(class_="top-item")
            items.extend(page.find_all(class_="card-wrapper"))
            items.extend(page.find_all(class_="card-buttons"))

            for item in items:
                string = item.find("a").get("href")
                match = pattern.search(string)
                if match:
                    nums.append(int(match.group(1)))

            if nums:
                return sorted(nums, reverse=True)

            raise ParsingError("An error occured while getting a page.")

        async def get_num_pages(self, data: ClientResponse) -> int:
            pattern = re.compile(r"=(\d+)")
            page = bs4.BeautifulSoup(await data.text(), features="lxml")

            if isinstance(item := page.find(class_="pagination"), bs4.Tag):
                links = item.find_all("a")
                string = links[-2].get("href")

                if match := pattern.search(string):
                    return int(match.group(1))

            raise ParsingError("An error occured while getting number of pages.")

    class ItemParser:
        async def create_item(self, data: ClientResponse) -> list[str]:
            page = bs4.BeautifulSoup(await data.text(), features="lxml")

            if isinstance(top_item := page.find(class_="top-item"), bs4.Tag):
                links = top_item.find_all("a")
                return [link.get("href") for link in links]
            raise ParsingError("An error occured while getting a card.")
