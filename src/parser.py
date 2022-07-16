from __future__ import annotations

import bs4
import re
import aiohttp
import asyncio

import utils
import consts

from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from classes import Card, Still, Item


class Parser(ABC):
    def set_session(self, session: aiohttp.ClientSession) -> None:
        self.session: aiohttp.ClientSession = session

    async def get_html(self, url: str) -> str:
        html: aiohttp.ClientResponse = await self.session.get(url)
        return await html.text()

    async def soup_page(self, num: int) -> bs4.BeautifulSoup:
        return bs4.BeautifulSoup(await self.get_html(
            self.get_url(num)), features="lxml")

    async def get_item(self, num: int) -> tuple[int, Item]:
        self.bs: bs4.BeautifulSoup = await self.soup_page(num)
        return self.create_item(num)

    @abstractmethod
    def create_item(self, num: int) -> tuple[int, Item]:
        ...

    @abstractmethod
    def get_url(self, num: int) -> str:
        ...


class ListParser(Parser):
    def __init__(self, still: bool = False):
        self.url: str = consts.CARDS_LIST_URL_TEMPLATE if not still else consts.STILLS_LIST_URL_TEMPLATE

    def get_url(self, num: int):
        return f"{self.url}{num}"

    async def get_page(self, num: int) -> list[int]:
        nums: list[int] = []
        p: re.Pattern = re.compile(r"/([0-9]+)/")

        page: bs4.BeautifulSoup = await self.soup_page(num)
        items: bs4.ResultSet = page.find_all(class_="top-item")

        for item in items:

            string: str = item.find("a").get("href")
            m: Optional[re.Match] = p.search(string)

            if m:
                g = m.group(1)
                nums.append(int(g))

        return sorted(nums, reverse=True)

    async def get_num_pages(self) -> int:
        p: re.Pattern = re.compile(r"=([0-9]+)")

        page: bs4.BeautifulSoup = await self.soup_page(1)
        item: bs4.Tag | bs4.NavigableString | None = page.find(
            class_="pagination")

        if isinstance(item, bs4.Tag):

            links: bs4.ResultSet = item.find_all("a")
            string: str = links[-2].get("href")

            m: Optional[re.Match] = p.search(string)

            if m:
                g = m.group(1)
        return int(g)

    def create_item(self, num: int) -> tuple[int, Item]:
        ...


class CardParser(Parser):

    def get_url(self, num: int) -> str:
        return f"{consts.CARD_URL_TEMPLATE}{num}"

    def create_item(self, num: int) -> tuple[int, Card]:
        from classes import Card
        urls: tuple[str, str] = self.get_item_image_urls()

        idol: str = self.get_item_info("idol")
        rarity: str = self.get_item_info("rarity")
        attr: str = self.get_item_info("attribute")
        unit: str = self.get_item_info("i_unit")
        sub: str = self.get_item_info("i_subunit")
        year: str = self.get_item_info("i_year")

        new_card: Card = Card(num, idol, rarity, attr, unit,
                              sub, year, urls[0], urls[1])
        return num, new_card

    def update_item(self, card: Card) -> None:
        card.normal_url, card.idolized_url = self.get_item_image_urls()

    def get_item_image_urls(self) -> tuple[str, str]:
        top_item: bs4.Tag | bs4.NavigableString | None = self.bs.find(
            class_="top-item")

        if isinstance(top_item, bs4.Tag):
            links: bs4.ResultSet = top_item.find_all("a")

        return (links[0].get("href"), links[1].get("href"))

    def get_data_field(self, field: str) -> Optional[bs4.Tag]:
        data: bs4.Tag | bs4.NavigableString | None = self.bs.find(
            attrs={"data-field": field})

        if isinstance(data, bs4.Tag):
            return data.find_all("td")[1]
        else:
            return None

    def get_item_info(self, info: str) -> str:
        if info == "idol":
            data: Optional[bs4.Tag] = self.get_data_field("idol")

            if isinstance(data, bs4.Tag):
                found_data: bs4.Tag | bs4.NavigableString | None = data.find(
                    "span")

                if isinstance(found_data, bs4.Tag):
                    text: str = found_data.get_text().partition("Open idol")[
                        0].strip()

            return text
        else:
            other: Optional[bs4.Tag] = self.get_data_field(info)
            if isinstance(other, bs4.Tag):
                return other.get_text().strip()
            else:
                return ""


class StillParser(Parser):

    def get_url(self, num: int) -> str:
        return f"{consts.STILL_URL_TEMPLATE}{num}"

    def create_item(self, num: int) -> tuple[int, Still]:
        from classes import Still
        url: str = self.get_item_image_url()

        new_item: Still = Still(
            num, url
        )
        return num, new_item

    def update_item(self, item: Still) -> None:
        item.url = self.get_item_image_url()

    def get_item_image_url(self) -> str:
        top_item: bs4.Tag | bs4.NavigableString | None = self.bs.find(
            class_="top-item")
        if isinstance(top_item, bs4.Tag):
            links = top_item.find_all("a")
        return links[0].get("href")
