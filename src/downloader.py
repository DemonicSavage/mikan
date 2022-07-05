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
        self.list_parser = ListParser()
        self.still = False

    def download_image(self, dest, url):
        with open(dest, 'wb') as f:
            response = self.session.get(f"https:{url}")
            f.write(response.content)

    def update_if_needed(self, key, item):
        if self.needs_update(item):
            old_url = self.get_url(item)
            self.item_parser.parse(key)
            self.item_parser.update_item(item)
            new_url = self.get_url(item)
            return (old_url != new_url)

    def download(self, path, key, item):
        updateable_item = self.update_if_needed(key, item)
        if updateable_item:
            self.update_json_file()
            print(f"Updated item {key}.")

        if not path.exists() or updateable_item:
            self.get_image(key, item)

    def get_new(self):
        num = 1
        self.list_parser.parse(num, self.still)

        while (page_items := self.list_parser.get_page()):
            page_items = sorted(page_items, reverse=True)

            for i in range(len(page_items)):
                if page_items[i] not in self.objs:
                    self.item_parser.parse(page_items[i])
                    n, item = self.item_parser.create_item()
                    self.objs[n] = item
                    print(f"Getting item {n}.")

            num += 1
            self.list_parser.parse(num, self.still)

    def download_multi(self):
        for key, item in self.objs.items():
            path = self.get_path(key, item)
            self.download(path, key, item)
        self.session.close()

    def update(self):
        print("Searching for new or missing items...")
        self.get_new()

        print("Checking if items can be updated to better resolution...")
        for n, item in self.objs.items():
            if self.update_if_needed(n, item):
                print(f"Updated item {n}.")

        self.update_json_file()
        print("Updated items database.")

    def update_json_file(self):
        self.stills = dict(sorted(self.objs.items(), reverse=True))
        json_utils.dump_to_file(json_utils.to_json(
            self.objs), self.path, self.still)


class CardDownloader(Downloader):
    def __init__(self, path):
        super().__init__(path)
        utils.init_path(Path(self.path).joinpath(consts.CARD_RESULTS_DIR))
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
            self.download_image(normal_path, item.normal_url)
            print(
                f"Downloaded card {key}, normal.")
            self.download_image(idolized_path, item.idolized_url)
            print(
                f"Downloaded card {key}, idolized.")
        except Exception as e:
            print(f"Couldn't download card {key}.")


class StillDownloader(Downloader):
    def __init__(self, path):
        super().__init__(path)
        utils.init_path(Path(self.path).joinpath(consts.STILL_RESULTS_DIR))
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
            self.download_image(path, item.url)
            print(
                f"Downloaded still {key}.")
        except Exception as e:
            print(f"Couldn't download still {key}.")
