import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
import operator

import utils
import json_utils
import consts
from parser import CardParser, ListParser
from classes import Card

class CardDownloader:

    def __init__(self, path):
        self.path= utils.init_path(Path(path))
        utils.init_path(Path(self.path).joinpath(consts.CARD_RESULTS_DIR))
        self.cards = {}

        self.list_parser = ListParser()
        self.card_parser = CardParser()

    def download_image(self, key, card, card_path, idolized=False):
        with open(card_path, 'wb') as f:
            response = requests.get(f"https:{card.idolized_url if idolized else card.normal_url}")
            f.write(response.content)
            print(f"Downloaded card with the id {key}, {'idolized' if idolized else 'normal'}.")

    def update_card_if_needed(self, key, card):
        if not card.is_double_sized() and card.rarity != "Rare":
            old_url = card.normal_url
            self.card_parser.parse(key)
            self.card_parser.update_card(card)
            return (old_url != card.normal_url)

    def download_card(self, key, card):
        file_name = f"{key}_{card.unit}_{card.idol}"
        base_path = Path(self.path).joinpath(consts.CARD_RESULTS_DIR)
        normal_path = base_path.joinpath(f"{file_name}_Normal{Path(card.normal_url).suffix}")
        idolized_path = base_path.joinpath(f"{file_name}_Idolized{Path(card.idolized_url).suffix}")

        updateable_card = self.update_card_if_needed(key, card)
        if updateable_card:
            self.update_json_file()
            print(f"Updated card {key}.")

        if not normal_path.exists() or updateable_card:
            self.download_image(key, card, normal_path, idolized=False)
            self.download_image(key, card, idolized_path, idolized=True)

    def download_cards(self):
        for key, card in self.cards.items():
            self.download_card(key, card)

    def get_new_cards(self):
        num = 1
        self.list_parser.parse(num)

        while (page_items := self.list_parser.get_page()):
            page_items = sorted(page_items, reverse=True)

            for i in range(len(page_items)):
                if page_items[i] not in self.cards:
                    self.card_parser.parse(page_items[i])
                    n, card = self.card_parser.create_card()  
                    self.cards[n] = card
                    print(f"Getting card {n}.")

            num += 1
            self.list_parser.parse(num)

    def update_cards(self):
        print("Searching for new or missing cards...")
        self.get_new_cards()

        print("Finding and updating non-double-sized SRs and URs to double-sized, if available...")
        for n, card in self.cards.items():
            if self.update_card_if_needed(n, card):
                print(f"Updated card {n}.")

        self.update_json_file()
        print("Updated cards.json file.")

    def update_json_file(self):
        self.cards = dict(sorted(self.cards.items(), reverse=True))
        json_utils.dump_to_file(json_utils.to_json(self.cards), self.path)