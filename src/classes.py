import re

from dataclasses import dataclass
from pathlib import Path

import consts
import parser
import organizer


@dataclass
class Idol:
    first_name: str
    last_name: str
    alt_spelling: str = None


@dataclass
class Group:
    name: str
    idols: list[Idol]


@dataclass
class Card:
    key: int
    idol: str
    rarity: str
    attribute: str
    unit: str
    subunit: str
    year: str
    normal_url: str
    idolized_url: str

    def is_double_sized(self):
        p = re.compile(r"/2x/")
        return p.search(self.normal_url) != None

    def get_urls(self):
        return [self.normal_url, self.idolized_url]

    def set_url(self, i, url):
        if i == 0:
            self.normal_url = url
        else:
            self.idolized_url = url

    def needs_update(self):
        return not self.is_double_sized() and self.rarity != "Rare"

    def get_paths(self, path):
        file_name = f"{self.key}_{self.unit}_{self.idol}"
        base_path = Path(path) / consts.CARD_RESULTS_DIR

        normal_path = f"{file_name}_Normal{Path(self.normal_url).suffix}"
        idolized_path = normal_path.replace("Normal", "Idolized")

        return [base_path / normal_path, base_path / idolized_path]

    @staticmethod
    def get_folder():
        return consts.CARD_RESULTS_DIR

    @staticmethod
    def get_parser():
        return parser.CardParser()

    @staticmethod
    def get_list_parser():
        return parser.ListParser()

    @staticmethod
    def get_json_filename():
        return "cards.json"

    @staticmethod
    def get_organizer(path):
        return organizer.CardOrganizer(path)


@dataclass
class Still:
    key: int
    url: str

    def is_double_sized(self):
        p = re.compile(r"/2x/")
        return p.search(self.url) != None

    def get_urls(self):
        return [self.url]

    def set_url(self, i, url):
        self.url = url

    def needs_update(self):
        return not self.is_double_sized()

    def get_paths(self, path):
        file_name = f"{self.key}_Still"
        base_path = Path(path) / consts.STILL_RESULTS_DIR

        return [base_path / f"{file_name}{Path(self.url).suffix}"]

    @staticmethod
    def get_folder():
        return consts.STILL_RESULTS_DIR

    @staticmethod
    def get_parser():
        return parser.StillParser()

    @staticmethod
    def get_list_parser():
        return parser.ListParser(still=True)

    @staticmethod
    def get_json_filename():
        return "stills.json"

    @staticmethod
    def get_organizer(path):
        return organizer.StillOrganizer(path)
