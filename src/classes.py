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

    def key(self):
        p = re.compile(r"/([0-9]+)[A-Z]")
        m = p.search(self.normal_url)
        g = m.group(1)
        return int(g)

    def get_urls(self):
        return [self.normal_url, self.idolized_url]

    def set_url(self, i, url):
        if i == 0:
            self.normal_url = url
        else:
            self.idolized_url = url

    def needs_update(self):
        return not self.is_double_sized() and self.rarity != "Rare"


@dataclass
class Still:
    url: str

    def is_double_sized(self):
        p = re.compile(r"/2x/")
        return p.search(self.url) != None

    def key(self):
        p = re.compile(r"/([0-9]+)[A-Z]")
        m = p.search(self.url)
        g = m.group(1)
        return int(g)

    def get_urls(self):
        return [self.url]

    def set_url(self, i, url):
        self.url = url

    def needs_update(self):
        return not self.is_double_sized()
