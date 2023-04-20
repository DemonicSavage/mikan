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

import re
from abc import ABC, abstractmethod
from typing import Optional

import aiohttp
import bs4

from mikan.classes import Card, Item, SIFCard, Still


class ListParsingException(Exception):
    pass


class ItemParsingException(Exception):
    pass


class NoHTTPSessionException(Exception):
    pass


class Parser(ABC):
    def __init__(self) -> None:
        self.session: Optional[aiohttp.ClientSession] = None
        self.soup: Optional[bs4.BeautifulSoup] = None

    def set_session(self, session: aiohttp.ClientSession) -> None:
        self.session = session

    async def get_html(self, url: str) -> str:
        if isinstance(self.session, aiohttp.ClientSession):
            html = await self.session.get(url)
            return await html.text()

        raise NoHTTPSessionException()

    async def soup_page(self, num: int) -> bs4.BeautifulSoup:
        return bs4.BeautifulSoup(
            await self.get_html(self.get_url(num)), features="lxml"
        )

    async def get_item(self, num: int) -> tuple[int, Item]:
        self.soup = await self.soup_page(num)

        return await self.create_item(num)

    @abstractmethod
    async def create_item(self, num: int) -> tuple[int, Item]:
        pass

    @abstractmethod
    def get_url(self, num: int) -> str:
        pass


class SIFListParser(Parser):
    def __init__(self) -> None:
        self.items: list[list[int]] = []

    async def get_items(self) -> None:
        if isinstance(self.session, aiohttp.ClientSession):
            html = await self.session.get("https://schoolido.lu/api/cardids/")
            json = await html.json()

            self.items = [json[i : i + 10] for i in range(0, len(json), 10)]  # noqa
        else:
            raise ListParsingException()

    async def get_page(self, num: int) -> list[int]:
        return self.items[num - 1]

    async def get_num_pages(self) -> int:
        await self.get_items()
        return len(self.items)

    async def create_item(self, num: int) -> tuple[int, Item]:
        pass

    def get_url(self, num: int) -> str:
        pass


class SIFCardParser(Parser):
    def get_url(self, num: int) -> str:
        pass

    async def create_item(self, num: int) -> tuple[int, SIFCard]:
        if isinstance(self.session, aiohttp.ClientSession):
            html = await self.session.get(f"https://schoolido.lu/api/cards/{num}/")
            json = await html.json()

            new_card = SIFCard(
                json["id"],
                json["idol"]["name"],
                json["rarity"],
                json["attribute"],
                json["idol"]["main_unit"],
                json["idol"]["sub_unit"],
                json["idol"]["year"],
                json["card_image"],
                json["card_idolized_image"],
            )

            return json["id"], new_card
        raise ItemParsingException()

    async def get_item(self, num: int) -> tuple[int, SIFCard]:
        return await self.create_item(num)


class ListParser(Parser):
    def __init__(self, img_type: type[Item]):
        super().__init__()
        self.url = img_type.list_url_template

    def get_url(self, num: int) -> str:
        return f"{self.url}{num}"

    async def get_page(self, num: int) -> list[int]:
        nums: list[int] = []
        pattern = re.compile(r"/(\d+)/")

        page = await self.soup_page(num)
        items = page.find_all(class_="top-item")

        for item in items:
            string = item.find("a").get("href")
            match = pattern.search(string)
            if match:
                nums.append(int(match.group(1)))

        if nums:
            return sorted(nums, reverse=True)

        raise ListParsingException()

    async def get_num_pages(self) -> int:
        pattern = re.compile(r"=(\d+)")
        page = await self.soup_page(1)

        if isinstance(item := page.find(class_="pagination"), bs4.Tag):
            links = item.find_all("a")
            string = links[-2].get("href")

            if match := pattern.search(string):
                return int(match.group(1))

        raise ListParsingException()

    async def create_item(self, num: int) -> tuple[int, Item]:
        pass


class CardParser(Parser):
    def get_url(self, num: int) -> str:
        return f"{Card.url_template}{num}"

    async def create_item(self, num: int) -> tuple[int, Card]:
        urls = self.get_item_image_urls()

        idol = self.get_data_field("idol")
        rarity = self.get_data_field("rarity")
        attr = self.get_data_field("attribute")
        unit = self.get_data_field("idol__i_unit")
        if unit and unit.startswith("Nijigasaki"):  # pragma: no cover
            unit = "Nijigasaki"
        sub = self.get_data_field("idol__i_subunit")
        year = self.get_data_field("idol__i_year")

        new_card = Card(num, idol, rarity, attr, unit, sub, year, urls[0], urls[1])

        return num, new_card

    def get_item_image_urls(self) -> tuple[str, str]:
        if self.soup and isinstance(
            top_item := self.soup.find(class_="top-item"), bs4.Tag
        ):
            links = top_item.find_all("a")
            first: str = links[0].get("href")
            second: str = links[1].get("href")

            return (first, second)

        raise ItemParsingException()

    def get_data_field(self, field: str) -> str:
        if (
            self.soup
            and isinstance(
                data_field := self.soup.find(attrs={"data-field": field}), bs4.Tag
            )
            and isinstance(
                data := [
                    x for x in data_field.get_text().strip().split("\n") if x != ""
                ][1],
                str,
            )
        ):
            return data
        raise ItemParsingException()


class StillParser(Parser):
    def get_url(self, num: int) -> str:
        return f"{Still.url_template}{num}"

    async def create_item(self, num: int) -> tuple[int, Still]:
        url = self.get_item_image_url()

        new_item = Still(num, url)

        return num, new_item

    def get_item_image_url(self) -> str:
        if self.soup and isinstance(
            top_item := self.soup.find(class_="top-item"), bs4.Tag
        ):
            links = top_item.find_all("a")
            if isinstance(link := links[0].get("href"), str):
                return link

        raise ItemParsingException()
