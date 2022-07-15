from __future__ import annotations

from bs4 import BeautifulSoup
from pathlib import Path
import re
import operator
import asyncio
import aiohttp


import utils
import json_utils
import consts
from classes import Item, Card
from parser import CardParser, StillParser, ListParser

from typing import Coroutine, Any


class Downloader:
    def __init__(self, path: Path, img_type: type[Item]):
        self.path: Path = utils.init_path(Path(path))
        self.objs: dict[int, Item] = {}

        self.img_type: type[Item] = img_type

        utils.init_path(Path(self.path) / self.img_type.get_folder())

        json_utils.load_cards(self.path, self.objs, img_type)

        self.list_parser: ListParser = self.img_type.get_list_parser()
        self.item_parser: CardParser | StillParser = self.img_type.get_parser()

        self.updateables: list[int] = []

    async def __aenter__(self) -> Downloader:
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()

        self.list_parser.set_session(self.session)
        self.item_parser.set_session(self.session)

        return self

    async def __aexit__(self, exc_type: None, exc_value: None, exc_traceback: None) -> None:
        await self.session.close()

    async def write_to_file(self, dest: Path, url: str) -> None:
        response: aiohttp.ClientResponse = await self.session.get(f"https:{url}")
        if response.status == 200:
            response_data: bytes = await response.read()
            with open(dest, 'wb') as f:
                f.write(response_data)

    async def get_images(self, item: Item) -> None:
        paths: list[Path] = item.get_paths(self.path)
        try:
            await self.download_images(paths, item)
        except Exception as e:
            print(f"Couldn't download card {item.key}: {e}.")

    async def create_image_file(self, path: Path, item: Item, i: int) -> None:
        if not path.exists() or item.key in self.updateables:
            await self.write_to_file(path, item.get_urls()[i])

            message: str = f"Downloaded item {item.key}"
            if type(item) is Card:
                message += f", {'idolized' if i == 1 else 'normal'}"
            message += "."

            print(message)

    async def download_images(self, paths: list[Path], item: Item) -> None:
        for i, path in enumerate(paths):
            await self.create_image_file(path, item, i)

    async def update_if_needed(self, item: Item) -> None:
        if item.needs_update():
            n, updated_item = await self.item_parser.get_item(item.key)

            if item.get_urls()[0] != updated_item.get_urls()[0]:
                self.updateables.append(item.key)

            for i in range(len(item.get_urls())):
                item.set_url(i, updated_item.get_urls()[i])

    async def add_item_to_object_list(self, item: int) -> None:
        n, obj = await self.item_parser.get_item(item)
        self.objs[n] = obj
        print(f"Getting item {n}.")

    async def get_page(self, idx: int) -> list[None]:
        tasks: list[Coroutine] = []
        page: list[int] = await self.list_parser.get_page(idx)
        for item in page:
            if item not in self.objs:

                tasks.append(
                    self.add_item_to_object_list(item))
        results: list[None] = await asyncio.gather(*tasks, return_exceptions=True)
        return results

    async def get_cards_from_parser(self) -> None:
        num_pages: int = await self.list_parser.get_num_pages()+1
        current_num: int = 1
        for i in range(1, num_pages):
            current_page: list[None] = await self.get_page(current_num)
            if not current_page:
                break
            current_num += 1

    async def download(self) -> None:
        tasks: list[Coroutine] = []
        for key, item in self.objs.items():
            tasks.append(self.get_images(item))
        await asyncio.gather(*tasks, return_exceptions=False)

    async def update(self) -> None:
        print("Searching for new or missing items...")
        await self.get_cards_from_parser()

        print("Checking if items can be updated to better resolution...")
        for key, item in self.objs.items():
            await self.update_if_needed(item)

        self.update_json_file()
        print("Updated items database.")

    def update_json_file(self) -> None:
        self.objs = dict(
            sorted(self.objs.items(), reverse=True))
        json_utils.dump_to_file(json_utils.to_json(
            self.objs), self.path, self.img_type)
