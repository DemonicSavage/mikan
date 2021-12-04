import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
import operator

import utils
import json_utils
import config
from parser import CardParser, ListParser
from classes import Card

class CardDownloader:

    def __init__(self, path):
        self.path= utils.init_path(Path(path))
        utils.init_path(Path(self.path).joinpath(config.CARD_RESULTS_DIR))
        self.cards = {}

        self.list_parser = ListParser()
        self.card_parser = CardParser()

    def download_image(self, key, card, card_path, idolized=False):
        with open(card_path, 'wb') as f:
            response = requests.get(f"https:{card.idolized_url if idolized else card.normal_url}")
            f.write(response.content)
            print(f"Downloaded card with the id {key}, {'idolized' if idolized else 'normal'}.")

    def update_card_if_needed(self, key, card):
        if card.needs_update:
            self.card_parser.parse(key)
            self.card_parser.update_card(card)
            card.needs_update = not card.is_double_sized() and card.rarity != "Rare"
            if not card.needs_update:
                print(f"Updated card with the id {key}.")

    def download_card(self, key, card):
        file_name = f"{key}_{card.unit}_{card.idol}"
        base_path = Path(self.path).joinpath(config.CARD_RESULTS_DIR)
        normal_path = base_path.joinpath(f"{file_name}_Normal{Path(card.normal_url).suffix}")
        idolized_path = base_path.joinpath(f"{file_name}_Idolized{Path(card.idolized_url).suffix}")

        if not normal_path.exists() or card.needs_update:
            self.update_card_if_needed(key, card)
            self.update_json_file()
            self.download_image(key, card, normal_path, idolized=False)
            self.download_image(key, card, idolized_path, idolized=True)

    def download_cards(self):
        for key, card in self.cards.items():
            self.download_card(key, card)

    def update_cards(self):
        num = 1
        already_exists = False
        self.list_parser.parse(num)

        while (page_items := self.list_parser.get_page()):
            page_items = sorted(page_items, reverse=True)

            for i in range(len(page_items)):
                self.card_parser.parse(page_items[i])
                n, card = self.card_parser.create_card()  

                if n not in self.cards:
                    self.cards[n] = card
                    print(f"Getting card {n}.")
                else:
                    already_exists = True
                    break

            if already_exists:
                break

            num += 1
            self.list_parser.parse(num)

        for num, card in self.cards.items():
            self.update_card_if_needed(num, card)

        self.update_json_file()

    def update_json_file(self):
        self.cards = dict(sorted(self.cards.items(), reverse=True))
        json_utils.dump_to_file(json_utils.to_json(self.cards), self.path)