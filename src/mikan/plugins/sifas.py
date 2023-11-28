from mikan.plugins.default import DefaultPlugin
from mikan.plugins.sif2 import SIF2


class SIFAS(SIF2, DefaultPlugin):
    card_dir = "SIFAS_Cards"
    url = "https://idol.st/ajax/allstars/card/"
    list_url = "https://idol.st/ajax/allstars/cards/?page="
    cli_arg = "sifas"
    desc = "SIFAS cards"
