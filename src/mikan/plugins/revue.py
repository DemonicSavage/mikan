import bs4
from aiohttp import ClientResponse

from mikan.html_parser import ParsingError
from mikan.plugins.default import DefaultPlugin
from mikan.plugins.sif2 import SIF2


class Revue(SIF2, DefaultPlugin):
    card_dir = "Revue_Cards"
    url = "https://starlight.academy/ajax/card/"
    list_url = "https://starlight.academy/ajax/cards/?page="
    cli_arg = "revue"
    desc = "Revue Starlight cards"

    class ItemParser:
        async def create_item(self, data: ClientResponse) -> list[str]:
            page = bs4.BeautifulSoup(await data.text(), features="lxml")

            if isinstance(top_item := page.find(attrs={"data-field": "art"}), bs4.Tag):
                links = top_item.find_all("a")
                return [link.get("href") for link in links]

            raise ParsingError("An error occured while getting a card.")
