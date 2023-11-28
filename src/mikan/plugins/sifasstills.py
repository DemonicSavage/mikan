import bs4
from aiohttp import ClientResponse

from mikan.html_parser import ParsingError
from mikan.plugins.default import DefaultPlugin
from mikan.plugins.sif2 import SIF2


class SIFASStills(SIF2, DefaultPlugin):
    card_dir = "SIFAS_Stills"
    url = "https://idol.st/ajax/allstars/still/"
    list_url = "https://idol.st/ajax/allstars/stills/?page="
    cli_arg = "stills"
    desc = "SIFAS stills"

    class ItemParser:
        async def create_item(self, data: ClientResponse) -> list[str]:
            page = bs4.BeautifulSoup(await data.text(), features="lxml")

            if isinstance(top_item := page.find(class_="top-item"), bs4.Tag):
                links = top_item.find_all("a")
                url: str = links[0].get("href")

                return [url]

            raise ParsingError("An error occured while getting a still.")
