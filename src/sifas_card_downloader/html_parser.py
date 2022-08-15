from __future__ import annotations

import re
from abc import ABC
from typing import Optional

import aiohttp
import bs4

from sifas_card_downloader.classes import Card, Item, Still


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

        return self.create_item(num)

    def create_item(self, num: int) -> tuple[int, Item]:
        ...

    def get_url(self, num: int) -> str:
        ...


class ListParser(Parser):
    def __init__(self, img_type: type[Item]):
        super().__init__()
        self.url = img_type.list_url_template

    def get_url(self, num: int) -> str:
        return f"{self.url}{num}"

    async def get_page(self, num: int) -> list[int]:
        nums: list[int] = []
        pattern = re.compile(r"/([0-9]+)/")

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
        pattern = re.compile(r"=([0-9]+)")
        page = await self.soup_page(1)

        if isinstance(item := page.find(class_="pagination"), bs4.Tag):
            links = item.find_all("a")
            string = links[-2].get("href")

            if match := pattern.search(string):
                return int(match.group(1))

        raise ListParsingException()

    def create_item(self, num: int) -> tuple[int, Item]:
        ...


class CardParser(Parser):
    def get_url(self, num: int) -> str:
        return f"{Card.url_template}{num}"

    def create_item(self, num: int) -> tuple[int, Card]:
        urls = self.get_item_image_urls()

        idol = self.get_item_info("idol")
        rarity = self.get_item_info("rarity")
        attr = self.get_item_info("attribute")
        unit = self.get_item_info("i_unit")
        sub = self.get_item_info("i_subunit")
        year = self.get_item_info("i_year")

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

    def get_data_field(self, field: str) -> bs4.Tag:

        if (
            self.soup
            and isinstance(data := self.soup.find(attrs={"data-field": field}), bs4.Tag)
            and isinstance(field := data.find_all("td")[1], bs4.Tag)
        ):
            return field

        raise ItemParsingException()

    def get_item_info(self, info: str) -> str:
        if info == "idol":
            data = self.get_data_field("idol")
            if isinstance(found_data := data.find("span"), bs4.Tag) and isinstance(
                text := found_data.get_text(), str
            ):

                return text.partition("Open idol")[0].strip()

        if isinstance(text := self.get_data_field(info).getText(), str):
            return text.strip()

        raise ItemParsingException()


class StillParser(Parser):
    def get_url(self, num: int) -> str:
        return f"{Still.url_template}{num}"

    def create_item(self, num: int) -> tuple[int, Still]:
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
