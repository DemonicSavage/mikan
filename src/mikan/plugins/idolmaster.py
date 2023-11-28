import bs4
from aiohttp import ClientResponse

from mikan.plugins.default import DefaultPlugin
from mikan.plugins.sif2 import SIF2


class Idolmaster(SIF2, DefaultPlugin):
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
