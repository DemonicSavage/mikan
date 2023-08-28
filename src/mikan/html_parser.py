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


import asyncio
import re
from typing import Any

import bs4
from aiohttp import ClientResponse, ClientSession

from mikan.classes import CardType, SIFCard, Still


class ParsingError(Exception):
    pass


class Parser:
    def __init__(self, objs: dict[str, dict[str, list[str]]], img_type: CardType, session: ClientSession) -> None:
        self.session: ClientSession = session
        self.img_type = img_type
        self.objs = objs

        self.list_parser: ListParser | SIFListParser = ListParser()
        self.item_parser: CardParser | StillParser | SIFCardParser = CardParser()

        if self.img_type == SIFCard:
            self.list_parser, self.item_parser = SIFListParser(), SIFCardParser()
        elif self.img_type == Still:
            self.item_parser = StillParser()

    async def get(self, url: str) -> ClientResponse:
        return await self.session.get(url)

    async def get_page(self, idx: int) -> list[None]:
        data = await self.get(f"{self.img_type.list_url_template}{idx}") if self.img_type != SIFCard else idx
        page = await self.list_parser.get_page(data)

        tasks = [self.add_to_objs(item) for item in page if str(item) not in self.objs[self.img_type.results_dir]]

        res: list[None] = await asyncio.gather(*tasks, return_exceptions=False)

        return res

    async def get_items(self) -> None:
        num_pages = await self.list_parser.get_num_pages(await self.get(self.img_type.list_url_template)) + 1
        current_num = 1
        for _ in range(1, num_pages):
            current_page = await self.get_page(current_num)
            if not current_page and self.img_type != SIFCard:
                break

            current_num += 1

    async def add_to_objs(self, item: int) -> None:
        obj = await self.item_parser.create_item(await self.get(f"{self.img_type.url_template}{item}"))
        self.objs[self.img_type.results_dir][str(item)] = obj
        print(f"Getting item {item}.")


class SIFListParser:
    def __init__(self) -> None:
        self.items: list[list[int]] = []

    async def get_page(self, num: Any) -> list[int]:
        return self.items[num - 1]

    async def get_num_pages(self, data: ClientResponse) -> int:
        json = await data.json()
        self.items = [json[i : i + 10] for i in range(0, len(json), 10)]
        return len(self.items)


class SIFCardParser:
    async def create_item(self, data: ClientResponse) -> list[str]:
        json = await data.json()
        return [card for card in [json["card_image"], json["card_idolized_image"]] if card]


class ListParser:
    async def get_page(self, data: Any) -> list[int]:
        nums: list[int] = []
        pattern = re.compile(r"/(\d+)/")

        page = bs4.BeautifulSoup(await data.text(), features="lxml")
        items = page.find_all(class_="top-item")

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


class CardParser:
    async def create_item(self, data: ClientResponse) -> list[str]:
        page = bs4.BeautifulSoup(await data.text(), features="lxml")

        if isinstance(top_item := page.find(class_="top-item"), bs4.Tag):
            links = top_item.find_all("a")
            first: str = links[0].get("href")
            second: str = links[1].get("href")

            return [first, second]

        raise ParsingError("An error occured while getting a card.")


class StillParser:
    async def create_item(self, data: ClientResponse) -> list[str]:
        page = bs4.BeautifulSoup(await data.text(), features="lxml")

        if isinstance(top_item := page.find(class_="top-item"), bs4.Tag):
            links = top_item.find_all("a")
            url: str = links[0].get("href")

            return [url]

        raise ParsingError("An error occured while getting a still.")
