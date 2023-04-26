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

from __future__ import annotations

import asyncio
import re
from typing import Any, Coroutine

import aiohttp
import bs4

from mikan.classes import Item, SIFCard, Still


class ListParsingException(Exception):
    pass


class ItemParsingException(Exception):
    pass


class Parser:
    def __init__(
        self,
        objs: dict[str, dict[str, list[str]]],
        img_type: type[Item],
        session: aiohttp.ClientSession,
    ) -> None:
        self.session: aiohttp.ClientSession = session
        self.img_type = img_type
        self.objs = objs

        self.list_parser: ListParser | SIFListParser = ListParser()
        self.item_parser: CardParser | StillParser | SIFCardParser = CardParser()

        if self.img_type == SIFCard:
            self.list_parser = SIFListParser()
            self.item_parser = SIFCardParser()
        elif self.img_type == Still:
            self.item_parser = StillParser()

    async def request_url_data(self, url: str) -> aiohttp.ClientResponse:
        return await self.session.get(url)

    async def get_page(self, idx: int) -> list[None]:
        tasks: list[Coroutine[Any, Any, None]] = []
        data = (
            await self.request_url_data(f"{self.img_type.list_url_template}{idx}")
            if self.img_type != SIFCard
            else idx
        )
        page = await self.list_parser.get_page(data)

        for item in page:
            if str(item) not in self.objs[self.img_type.results_dir]:
                tasks.append(self.add_item_to_object_list(item))

        res: list[None] = await asyncio.gather(*tasks, return_exceptions=False)

        return res

    async def get_cards_from_pages(self) -> None:
        num_pages = (
            await self.list_parser.get_num_pages(
                await self.request_url_data(self.img_type.list_url_template)
            )
            + 1
        )
        current_num = 1
        for _ in range(1, num_pages):
            current_page = await self.get_page(current_num)
            if not current_page and self.img_type != SIFCard:
                break

            current_num += 1

    async def add_item_to_object_list(self, item: int) -> None:
        i, obj = await self.item_parser.create_item(
            await self.request_url_data(f"{self.img_type.url_template}{item}")
        )
        self.objs[self.img_type.results_dir][i] = obj
        print(f"Getting item {i}.")


class SIFListParser:
    def __init__(self) -> None:
        self.items: list[list[int]] = []

    async def get_page(self, num: Any) -> list[int]:
        return self.items[num - 1]

    async def get_num_pages(self, data: aiohttp.ClientResponse) -> int:
        json = await data.json()
        self.items = [json[i : i + 10] for i in range(0, len(json), 10)]  # noqa
        return len(self.items)


class SIFCardParser:
    async def create_item(self, data: aiohttp.ClientResponse) -> tuple[str, list[str]]:
        json = await data.json()
        return str(json["id"]), [
            card for card in [json["card_image"], json["card_idolized_image"]] if card
        ]


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

        raise ListParsingException("An error occured while getting a page.")

    async def get_num_pages(self, data: aiohttp.ClientResponse) -> int:
        pattern = re.compile(r"=(\d+)")
        page = bs4.BeautifulSoup(await data.text(), features="lxml")

        if isinstance(item := page.find(class_="pagination"), bs4.Tag):
            links = item.find_all("a")
            string = links[-2].get("href")

            if match := pattern.search(string):
                return int(match.group(1))

        raise ListParsingException("An error occured while getting number of pages.")


class CardParser:
    async def create_item(self, data: aiohttp.ClientResponse) -> tuple[str, list[str]]:
        page = bs4.BeautifulSoup(await data.text(), features="lxml")
        pattern = re.compile(r"(\d+)")

        if isinstance(top_item := page.find(class_="top-item"), bs4.Tag):
            links = top_item.find_all("a")
            first: str = links[0].get("href")
            second: str = links[1].get("href")

            if match := pattern.search(first.split("/")[-1]):
                return match.group(1), [first, second]

        raise ItemParsingException("An error occured while getting a card.")


class StillParser:
    async def create_item(self, data: aiohttp.ClientResponse) -> tuple[str, list[str]]:
        page = bs4.BeautifulSoup(await data.text(), features="lxml")
        pattern = re.compile(r"(\d+)")

        if isinstance(top_item := page.find(class_="top-item"), bs4.Tag):
            links = top_item.find_all("a")
            url: str = links[0].get("href")

            if match := pattern.search(url.split("/")[-1]):
                return match.group(1), [url]

        raise ItemParsingException("An error occured while getting a still.")
