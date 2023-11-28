from mikan.plugins.base import Plugin
from mikan.plugins.sif2 import SIF2


class SIFAS(SIF2, Plugin):
    card_dir = "SIFAS_Cards"
    url = "https://idol.st/ajax/allstars/card/"
    list_url = "https://idol.st/ajax/allstars/cards/?page="
    cli_arg = "sifas"
    desc = "SIFAS cards"
