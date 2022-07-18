from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, cast

import aiohttp
import bs4

import consts

if TYPE_CHECKING:
    from classes import Card, Item, Still


class Parser(ABC):
    def __init__(self) -> None:
        self.session: Optional[aiohttp.ClientSession] = None
        self.soup: Optional[bs4.BeautifulSoup] = None

    def set_session(self, session: aiohttp.ClientSession) -> None:
        self.session = session

    async def get_html(self, url: str) -> str:
        if isinstance(self.session, aiohttp.ClientSession):
            html: aiohttp.ClientResponse = await self.session.get(url)

        return await html.text()

    async def soup_page(self, num: int) -> bs4.BeautifulSoup:
        return bs4.BeautifulSoup(
            await self.get_html(self.get_url(num)), features="lxml"
        )

    async def get_item(self, num: int) -> tuple[int, Item]:
        self.soup = await self.soup_page(num)
        return self.create_item(num)

    @abstractmethod
    def create_item(self, num: int) -> tuple[int, Item]:
        ...

    @abstractmethod
    def get_url(self, num: int) -> str:
        ...


class ListParser(Parser):
    def __init__(self, img_type: type[Item]):
        super().__init__()
        self.url: str = img_type.get_list_template()

    def get_url(self, num: int) -> str:
        return f"{self.url}{num}"

    async def get_page(self, num: int) -> list[int]:
        nums: list[int] = []
        pattern: re.Pattern[str] = re.compile(r"/([0-9]+)/")

        page: bs4.BeautifulSoup = await self.soup_page(num)
        items: bs4.ResultSet[bs4.Tag] = page.find_all(class_="top-item")

        for item in items:
            if (
                isinstance(item, bs4.Tag)
                and isinstance(found := item.find("a"), bs4.Tag)
                and isinstance(string := found.get("href"), str)
                and isinstance(match := pattern.search(string), re.Match)
            ):
                group: str = match.group(1)
                nums.append(int(group))

        return sorted(nums, reverse=True)

    async def get_num_pages(self) -> int:
        pattern: re.Pattern[str] = re.compile(r"=([0-9]+)")

        page: bs4.BeautifulSoup = await self.soup_page(1)
        if (
            isinstance(item := page.find(class_="pagination"), bs4.Tag)
            and isinstance(links := item.find_all("a"), bs4.ResultSet)
            and isinstance(string := links[-2].get("href"), str)
            and isinstance(match := pattern.search(string), re.Match)
        ):
            group: str = match.group(1)

        return int(group)

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

        new_card: Card = Card(
            num, idol, rarity, attr, unit, sub, year, urls[0], urls[1]
        )
        return num, new_card

    def update_item(self, card: Card) -> None:
        card.normal_url, card.idolized_url = self.get_item_image_urls()

    def get_item_image_urls(self) -> tuple[str, str]:
        if (
            isinstance(self.soup, bs4.BeautifulSoup)
            and isinstance(top_item := self.soup.find(class_="top-item"), bs4.Tag)
            and isinstance(links := top_item.find_all("a"), bs4.ResultSet)
            and isinstance(first := links[0].get("href"), str)
            and isinstance(second := links[1].get("href"), str)
        ):
            urls: tuple[str, str] = (first, second)
        return urls

    def get_data_field(self, field: str) -> bs4.Tag:

        if (
            isinstance(self.soup, bs4.BeautifulSoup)
            and isinstance(data := self.soup.find(attrs={"data-field": field}), bs4.Tag)
            and isinstance(res := data.find_all("td")[1], bs4.Tag)
        ):
            pass
        return cast(bs4.Tag, res)

    def get_item_info(self, info: str) -> str:
        if info == "idol":
            data: bs4.Tag = self.get_data_field("idol")

            if isinstance(found_data := data.find("span"), bs4.Tag):
                return found_data.get_text().partition("Open idol")[0].strip()

        return self.get_data_field(info).get_text().strip()


class StillParser(Parser):
    def get_url(self, num: int) -> str:
        return f"{consts.STILL_URL_TEMPLATE}{num}"

    def create_item(self, num: int) -> tuple[int, Still]:
        from classes import Still

        url: str = self.get_item_image_url()

        new_item: Still = Still(num, url)
        return num, new_item

    def update_item(self, item: Still) -> None:
        item.url = self.get_item_image_url()

    def get_item_image_url(self) -> str:
        if (
            isinstance(self.soup, bs4.BeautifulSoup)
            and isinstance(top_item := self.soup.find(class_="top-item"), bs4.Tag)
            and isinstance(links := top_item.find_all("a"), bs4.Tag)
        ):
            link: str = links[0].get("href")

        return link
