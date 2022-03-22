import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
import operator

import utils
import json_utils
import consts
from parser import CardParser, ListParser, StillParser
from classes import Card, Still


class CardDownloader:

    def __init__(self, path):
        self.path = utils.init_path(Path(path))
        utils.init_path(Path(self.path).joinpath(consts.CARD_RESULTS_DIR))
        self.objs = {}

        self.session = requests.Session()

        self.list_parser = ListParser()
        self.card_parser = CardParser()

    def download_image(self, key, card, card_path, idolized=False):
        with open(card_path, 'wb') as f:
            response = self.session.get(
                f"https:{card.idolized_url if idolized else card.normal_url}")
            f.write(response.content)
            print(
                f"Downloaded card {key}, {'idolized' if idolized else 'normal'}.")

    def update_if_needed(self, key, card):
        if not card.is_double_sized() and card.rarity != "Rare":
            old_url = card.normal_url
            self.card_parser.parse(key)
            self.card_parser.update_card(card)
            return (old_url != card.normal_url)

    def download(self, key, card):
        file_name = f"{key}_{card.unit}_{card.idol}"
        base_path = Path(self.path).joinpath(consts.CARD_RESULTS_DIR)
        normal_path = base_path.joinpath(
            f"{file_name}_Normal{Path(card.normal_url).suffix}")
        idolized_path = base_path.joinpath(
            f"{file_name}_Idolized{Path(card.idolized_url).suffix}")

        updateable_card = self.update_if_needed(key, card)
        if updateable_card:
            self.update_json_file()
            print(f"Updated card {key}.")

        if not normal_path.exists() or updateable_card:
            self.download_image(key, card, normal_path, idolized=False)
            self.download_image(key, card, idolized_path, idolized=True)

    def download_multi(self):
        for key, card in self.objs.items():
            self.download(key, card)
        self.session.close()

    def get_new(self):
        num = 1
        self.list_parser.parse(num)

        while (page_items := self.list_parser.get_page()):
            page_items = sorted(page_items, reverse=True)

            for i in range(len(page_items)):
                if page_items[i] not in self.objs:
                    self.card_parser.parse(page_items[i])
                    n, card = self.card_parser.create_card()
                    self.objs[n] = card
                    print(f"Getting card {n}.")

            num += 1
            self.list_parser.parse(num)

    def update(self):
        print("Searching for new or missing cards...")
        self.get_new()

        print("Checking if cards can be updated to better resolution...")
        for n, card in self.objs.items():
            if self.update_if_needed(n, card):
                print(f"Updated card {n}.")

        self.update_json_file()
        print("Updated cards database.")

    def update_json_file(self):
        self.objs = dict(sorted(self.objs.items(), reverse=True))
        json_utils.dump_to_file(json_utils.to_json(self.objs), self.path)


class StillDownloader:

    def __init__(self, path):
        self.path = utils.init_path(Path(path))
        utils.init_path(Path(self.path).joinpath(consts.STILL_RESULTS_DIR))
        self.objs = {}

        self.session = requests.Session()

        self.list_parser = ListParser()
        self.obj_parser = StillParser()

    def download_image(self, key, still, still_path):
        with open(still_path, 'wb') as f:
            response = self.session.get(f"https:{still.url}")
            f.write(response.content)
            print(f"Downloaded still {key}.")

    def update_if_needed(self, key, still):
        if not still.is_double_sized():
            old_url = still.url
            self.obj_parser.parse(key)
            self.obj_parser.update_still(still)
            return (old_url != still.url)

    def download(self, key, still):
        file_name = f"{key}_Still{Path(still.url).suffix}"
        base_path = Path(self.path).joinpath(consts.STILL_RESULTS_DIR)
        path = base_path.joinpath(f"{file_name}")

        updateable_still = self.update_if_needed(key, still)
        if updateable_still:
            self.update_json_file()
            print(f"Updated still {key}.")

        if not path.exists() or updateable_still:
            self.download_image(key, still, path)

    def download_multi(self):
        for key, still in self.objs.items():
            self.download(key, still)
        self.session.close()

    def get_new(self):
        num = 1
        self.list_parser.parse(num, still=True)

        while (page_items := self.list_parser.get_page()):
            page_items = sorted(page_items, reverse=True)

            for i in range(len(page_items)):
                if page_items[i] not in self.objs:
                    self.obj_parser.parse(page_items[i])
                    n, still = self.obj_parser.create_still()
                    self.objs[n] = still
                    print(f"Getting still {n}.")

            num += 1
            self.list_parser.parse(num, still=True)

    def update(self):
        print("Searching for new or missing still...")
        self.get_new()

        print("Checking if stills can be updated to better resolution...")
        for n, still in self.objs.items():
            if self.update_if_needed(n, still):
                print(f"Updated still {n}.")

        self.update_json_file()
        print("Updated stills database.")

    def update_json_file(self):
        self.stills = dict(sorted(self.objs.items(), reverse=True))
        json_utils.dump_to_file(json_utils.to_json(
            self.objs), self.path, still=True)
