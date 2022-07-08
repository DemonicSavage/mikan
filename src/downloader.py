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


class Downloader:
    def __init__(self, path):
        self.path = utils.init_path(Path(path))
        self.objs = {}

        self.session = requests.Session()
        self.still = False

    def write_to_file(self, dest, url):
        with open(dest, 'wb') as f:
            response = self.session.get(f"https:{url}")
            f.write(response.content)

    def update_if_needed(self, key, item):
        if self.needs_update(item):
            old_url = self.get_url(item)

            _, updated_item = self.item_parser.get_item(key)
            self.item_parser.update_item(updated_item)

            new_url = self.get_url(updated_item)

            return (old_url != new_url)

    def download_image(self, path, key, item):
        updateable_item = self.update_if_needed(key, item)
        if updateable_item:
            self.update_json_file()
            print(f"Updated item {key}.")

        if not path.exists() or updateable_item:
            self.get_image(key, item)

    def get_cards_from_parser(self):
        page_num = 1

        while (page_items := self.list_parser.get_page(page_num)):

            for item in page_items:
                if item not in self.objs:
                    n, obj = self.item_parser.get_item(item)
                    self.objs[n] = obj
                    print(f"Getting item {n}.")

            page_num += 1

    def download(self):
        for key, item in self.objs.items():
            path = self.get_path(key, item)
            self.download_image(path, key, item)
        self.session.close()

    def update(self):
        print("Searching for new or missing items...")
        self.get_cards_from_parser()

        print("Checking if items can be updated to better resolution...")
        for n, item in self.objs.items():
            if self.update_if_needed(n, item):
                print(f"Updated item {n}.")

        self.update_json_file()
        print("Updated items database.")

    def update_json_file(self):
        self.objs = dict(sorted(self.objs.items(), reverse=True))
        json_utils.dump_to_file(json_utils.to_json(
            self.objs), self.path, self.still)


class CardDownloader(Downloader):
    def __init__(self, path):
        super().__init__(path)
        utils.init_path(Path(self.path).joinpath(consts.CARD_RESULTS_DIR))
        self.list_parser = ListParser()
        self.item_parser = CardParser()

    def needs_update(self, item):
        return not item.is_double_sized() and item.rarity != "Rare"

    def get_url(self, item):
        return item.normal_url

    def get_path(self, key, item):
        file_name = f"{key}_{item.unit}_{item.idol}"
        base_path = Path(self.path).joinpath(consts.CARD_RESULTS_DIR)

        return base_path.joinpath(f"{file_name}_Normal{Path(item.normal_url).suffix}")

    def get_image(self, key, item):
        normal_path = str(self.get_path(key, item))
        idolized_path = normal_path.replace("Normal", "Idolized")
        try:
            self.write_to_file(normal_path, item.normal_url)
            print(
                f"Downloaded card {key}, normal.")
            self.write_to_file(idolized_path, item.idolized_url)
            print(
                f"Downloaded card {key}, idolized.")
        except Exception as e:
            print(f"Couldn't download card {key}.")


class StillDownloader(Downloader):
    def __init__(self, path):
        super().__init__(path)
        utils.init_path(Path(self.path).joinpath(consts.STILL_RESULTS_DIR))

        self.list_parser = ListParser(still=True)
        self.item_parser = StillParser()
        self.still = True

    def needs_update(self, item):
        return not item.is_double_sized()

    def get_url(self, item):
        return item.url

    def get_path(self, key, item):
        file_name = f"{key}_Still"
        base_path = Path(self.path).joinpath(consts.STILL_RESULTS_DIR)

        return base_path.joinpath(f"{file_name}{Path(item.url).suffix}")

    def get_image(self, key, item):
        path = str(self.get_path(key, item))
        try:
            self.write_to_file(path, item.url)
            print(
                f"Downloaded still {key}.")
        except Exception as e:
            print(f"Couldn't download still {key}.")
