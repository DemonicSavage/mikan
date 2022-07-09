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

        self.updateables = []

    def write_to_file(self, dest, url):
        with open(dest, 'wb') as f:
            response = self.session.get(f"https:{url}")
            f.write(response.content)

    def get_images(self, item):
        paths = self.get_paths(item)
        try:
            self.download_images(paths, item)
        except Exception as e:
            print(f"Couldn't download card {item.key}: {e}.")

    def create_image_file(self, path, item, i):
        if not Path(path).exists() or item.key in self.updateables:
            self.write_to_file(Path(path), item.get_urls()[i])

            message = f"Downloaded item {item.key}"
            if type(item) is Card:
                message += f", {'idolized' if i == 1 else 'normal'}"
            message += "."

            print(message)

    def download_images(self, paths, item):
        for i, path in enumerate(paths):
            self.create_image_file(path, item, i)

    def update_if_needed(self, item):
        if item.needs_update():
            n, updated_item = self.item_parser.get_item(item.key)

            if item.get_urls()[0] != updated_item.get_urls()[0]:
                self.updateables.append(item.key)

            for i in range(len(item.get_urls())):
                item.set_url(i, updated_item.get_urls()[i])

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
            self.get_images(item)
        self.session.close()

    def update(self):
        print("Searching for new or missing items...")
        self.get_cards_from_parser()

        print("Checking if items can be updated to better resolution...")
        for key, item in self.objs.items():
            self.update_if_needed(item)

        self.update_json_file()
        print("Updated items database.")

    def update_json_file(self):
        self.objs = dict(sorted(self.objs.items(), reverse=True))
        json_utils.dump_to_file(json_utils.to_json(
            self.objs), self.path, self.still)


class CardDownloader(Downloader):
    def __init__(self, path):
        super().__init__(path)
        utils.init_path(Path(self.path) / consts.CARD_RESULTS_DIR)
        self.list_parser = ListParser()
        self.item_parser = CardParser()

    def get_paths(self, item):
        file_name = f"{item.key}_{item.unit}_{item.idol}"
        base_path = Path(self.path) / consts.CARD_RESULTS_DIR

        normal_path = f"{file_name}_Normal{Path(item.normal_url).suffix}"
        idolized_path = normal_path.replace("Normal", "Idolized")

        return [base_path / normal_path, base_path / idolized_path]


class StillDownloader(Downloader):
    def __init__(self, path):
        super().__init__(path)
        utils.init_path(Path(self.path) / consts.STILL_RESULTS_DIR)

        self.list_parser = ListParser(still=True)
        self.item_parser = StillParser()
        self.still = True

    def get_paths(self, item):
        file_name = f"{item.key}_Still"
        base_path = Path(self.path) / consts.STILL_RESULTS_DIR

        return [base_path / f"{file_name}{Path(item.url).suffix}"]
