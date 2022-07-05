import re

from dataclasses import dataclass


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


@dataclass
class Still:
    url: str

    def is_double_sized(self):
        p = re.compile(r"/2x/")
        return p.search(self.url) != None
