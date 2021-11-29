from bs4 import BeautifulSoup
import re
import requests

import utils
import config
from classes import Card
from abc import ABC, abstractmethod


class Parser(ABC):
    def get_html(self, url):
        return requests.get(url).content

    @abstractmethod
    def get_url(self, num):
        pass

class ListParser(Parser):
    def __init__(self, num):
        self.bs = BeautifulSoup(super().get_html(self.get_url(num)), features="lxml")
        self.num = num

    def get_url(self, num):
        return f"{config.CARDS_LIST_URL_TEMPLATE}{num}"

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

    def __init__(self, num):
        self.bs = BeautifulSoup(super().get_html(self.get_url(num)), features="lxml")
        self.num = num

    def get_url(self, num):
        return f"{config.CARD_URL_TEMPLATE}{num}"

    def create_card(self) -> Card:
        return Card(
            self.num,
            self.get_card_info("idol"),
            self.get_card_info("rarity"),
            self.get_card_info("attribute"),
            self.get_card_info("i_unit"),
            self.get_card_info("i_subunit"),
            self.get_card_info("i_year"),
            self.get_card_info("urls")[0],
            self.get_card_info("urls")[1]
        )

    def get_card_image_urls(self):
        top_item = self.bs.find(class_="top-item")
        links = top_item.find_all("a")
        return (links[0].get("href"), links[1].get("href"))

    def get_data_field(self, field):
        data = self.bs.find(attrs={"data-field":field})
        if data:
            return data.find_all("td")[1]
        else:
            return None
    
    def get_card_info(self, info):
        if info == "idol":
            data = self.get_data_field("idol").find("span").get_text()
            data = data.partition("Open idol")[0].strip()
            return data
        elif info == "urls":
            return self.get_card_image_urls()       
        else:
            data = self.get_data_field(info)
            if data:
                return data.get_text().strip()
            else:
                return ""