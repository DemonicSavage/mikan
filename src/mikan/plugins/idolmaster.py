import re
from typing import Any

import bs4
from aiohttp import ClientResponse

from mikan.html_parser import ParsingError
from mikan.plugins.default import DefaultPlugin


class Idolmaster(DefaultPlugin):
    card_dir = "Idolmaster_Cards"
    url = "https://cinderella.pro/ajax/card/"
    list_url = "https://cinderella.pro/ajax/cards/?page="
    cli_arg = "idolmaster"
    desc = "Idolmaster Cinderella Girls cards"

    @staticmethod
    def item_renamer_fn(url: str) -> str:
        if "/a/" in url:
            name = url.split("/")[-1]
            stem = name.split(".")[-2]
            suffix = name.split(".")[-1]
            return f"{stem}_a.{suffix}"
        return url.split("/")[-1]

    class ListParser:
        async def get_page(self, data: Any) -> list[int]:
            nums: list[int] = []
            pattern = re.compile(r"/(\d+)/")

            page = bs4.BeautifulSoup(await data.text(), features="lxml")
            items = page.find_all(class_="card-buttons")

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

            items = page.find_all(class_="btn-sm")
            urls = []
            for item in items:
                href = item.get("href")
                if "/art/" in href or "/art_hd/" in href:
                    urls.append(href)

            return urls
