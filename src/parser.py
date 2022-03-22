from bs4 import BeautifulSoup
import re
import requests

import utils
import consts
from classes import Card, Still
from abc import ABC, abstractmethod


class Parser(ABC):
    bs: BeautifulSoup()
    num: int

    session = requests.Session()

    def get_html(self, url):
        return self.session.get(url).content

    def parse(self, num, still=False):
        self.bs = BeautifulSoup(self.get_html(
            self.get_url(num, still)), features="lxml")
        self.num = num


class ListParser(Parser):
    def get_url(self, num, still=False):
        return f"{consts.CARDS_LIST_URL_TEMPLATE}{num}" if not still else f"{consts.STILLS_LIST_URL_TEMPLATE}{num}"

    def get_page(self):
        nums = []
        p = re.compile(r"/([0-9]+)/")
        items = self.bs.find_all(class_="top-item")
        for item in items:
            string = item.find("a").get("href")
            m = p.search(string)
            g = m.group(1)
            nums.append(int(g))
        return nums


class CardParser(Parser):
    def get_url(self, num, still):
        return f"{consts.CARD_URL_TEMPLATE}{num}"

    def create_card(self) -> (int, Card):
        new_card = Card(
            self.get_card_info("idol"),
            self.get_card_info("rarity"),
            self.get_card_info("attribute"),
            self.get_card_info("i_unit"),
            self.get_card_info("i_subunit"),
            self.get_card_info("i_year"),
            self.get_card_image_urls()[0],
            self.get_card_image_urls()[1]
        )
        return self.num, new_card

    def update_card(self, card):
        card.normal_url, card.idolized_url = self.get_card_image_urls()

    def get_card_image_urls(self):
        top_item = self.bs.find(class_="top-item")
        links = top_item.find_all("a")
        return (links[0].get("href"), links[1].get("href"))

    def get_still_image_url(self):
        top_item = self.bs.find(class_="top-item")
        links = top_item.find_all("a")
        return links[0].get("href")

    def get_data_field(self, field):
        data = self.bs.find(attrs={"data-field": field})
        if data:
            return data.find_all("td")[1]
        else:
            return None

    def get_card_info(self, info):
        if info == "idol":
            data = self.get_data_field("idol").find("span").get_text()
            data = data.partition("Open idol")[0].strip()
            return data
        else:
            data = self.get_data_field(info)
            if data:
                return data.get_text().strip()
            else:
                return ""


class StillParser(Parser):
    def get_url(self, num, still):
        return f"{consts.STILL_URL_TEMPLATE}{num}"

    def create_still(self) -> (int, Still):
        new_still = Still(
            self.get_still_image_url()
        )
        return self.num, new_still

    def update_still(self, still):
        still.url = self.get_still_image_url()

    def get_still_image_url(self):
        top_item = self.bs.find(class_="top-item")
        links = top_item.find_all("a")
        return links[0].get("href")
