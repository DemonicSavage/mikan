import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
import json
import operator

import utils
import config
from parser import CardParser, ListParser
from classes import Card

class CardDownloader:

    def __init__(self, path):
        self.path= utils.init_path(Path(path))
        utils.init_path(Path(self.path).joinpath(config.CARD_RESULTS_DIR))
        self.data = []
        self.cards = []
    
    def download_image(self, url, name):
        card_path = Path(self.path).joinpath(config.CARD_RESULTS_DIR).joinpath(name)
        if not card_path.exists():
            with open(card_path, 'wb') as f:
                response = requests.get(f"https:{url}")
                f.write(response.content)
                print(f"Downloaded card {name}")
        else:
            print(f"Card {name} has already been downloaded")

    def download_card(self, card):
        name = f"{card.num}_{card.unit}_{card.idol}"

        self.download_image(card.normal_url, f"{name}_Normal{Path(card.normal_url).suffix}")
        self.download_image(card.idolized_url, f"{name}_Idolized{Path(card.idolized_url).suffix}")

    def download_cards(self):
        for card in self.cards:
            self.download_card(card)

    def update_cards(self):
        num = 1
        already_exists = False
        while (page_items := ListParser(num).get_page()):
            page_items = sorted(page_items, reverse=True)
            for i in range(len(page_items)):
                parser = CardParser(page_items[i])
                card = parser.create_card()
                if card not in self.cards:
                    self.cards.append(card)
                    print(f"Getting card {i+1} of {len(page_items)} from page {num}.")
                else:
                    already_exists = True
                    break
            if already_exists:
                break
            num += 1
        self.cards.sort(key=lambda x: x.num, reverse=True)
        self.dump_to_file(self.to_json())

    def to_json(self):
        return json.dumps([card.__dict__ for card in self.cards], ensure_ascii=False, indent=4)

    def dump_to_file(self, json_obj):
        card_path = Path(self.path).joinpath("cards.json")
        with open(card_path, "w") as f:
            f.write(json_obj)

    def read_json_file(self):
        card_path = Path(self.path).joinpath("cards.json")
        with open(card_path, "r") as f:
            data = f.read()
        cards = json.loads(data)
        for card in cards:
            self.cards.append(Card(**card))

    def load_cards(self):
        card_path = Path(self.path).joinpath("cards.json")
        if card_path.is_file():
            self.read_json_file()
        