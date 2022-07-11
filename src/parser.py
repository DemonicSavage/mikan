from bs4 import BeautifulSoup
import re
import aiohttp
import asyncio

import utils
import consts


class Parser():
    def set_session(self, session):
        self.session = session

    async def get_html(self, url):
        html = await self.session.get(url)
        return await html.text()

    async def soup_page(self, num):
        return BeautifulSoup(await self.get_html(
            self.get_url(num)), features="lxml")

    async def get_item(self, num):
        self.bs = await self.soup_page(num)
        return self.create_item(num)


class ListParser(Parser):
    def __init__(self, still=False):
        self.url = consts.CARDS_LIST_URL_TEMPLATE if not still else consts.STILLS_LIST_URL_TEMPLATE

    def get_url(self, num):
        return f"{self.url}{num}"

    async def get_page(self, num):
        nums = []
        p = re.compile(r"/([0-9]+)/")
        page = await self.soup_page(num)
        items = page.find_all(class_="top-item")
        for item in items:
            string = item.find("a").get("href")
            m = p.search(string)
            g = m.group(1)
            nums.append(int(g))
        return sorted(nums, reverse=True)

    async def get_num_pages(self):
        p = re.compile(r"=([0-9]+)")
        page = await self.soup_page(1)
        item = page.find(class_="pagination")
        links = item.find_all("a")
        string = links[-2].get("href")
        m = p.search(string)
        g = m.group(1)
        return int(g)


class CardParser(Parser):

    def get_url(self, num):
        return f"{consts.CARD_URL_TEMPLATE}{num}"

    def create_item(self, num):
        from classes import Card
        new_card = Card(
            num,
            self.get_item_info("idol"),
            self.get_item_info("rarity"),
            self.get_item_info("attribute"),
            self.get_item_info("i_unit"),
            self.get_item_info("i_subunit"),
            self.get_item_info("i_year"),
            self.get_item_image_urls()[0],
            self.get_item_image_urls()[1]
        )
        return num, new_card

    def update_item(self, card):
        card.normal_url, card.idolized_url = self.get_item_image_urls()

    def get_item_image_urls(self):
        top_item = self.bs.find(class_="top-item")
        links = top_item.find_all("a")
        return (links[0].get("href"), links[1].get("href"))

    def get_data_field(self, field):
        data = self.bs.find(attrs={"data-field": field})
        if data:
            return data.find_all("td")[1]
        else:
            return None

    def get_item_info(self, info):
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

    def get_url(self, num):
        return f"{consts.STILL_URL_TEMPLATE}{num}"

    def create_item(self, num):
        from classes import Still
        new_item = Still(
            num,
            self.get_item_image_url()
        )
        return num, new_item

    def update_item(self, item):
        item.url = self.get_item_image_url()

    def get_item_image_url(self):
        top_item = self.bs.find(class_="top-item")
        links = top_item.find_all("a")
        return links[0].get("href")
