from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Coroutine

import aiohttp

import json_utils
import utils
from classes import Card, Item
from html_parser import CardParser, ListParser, StillParser


class Downloader:
    def __init__(self, path: Path, img_type: type[Item]):
        self.path: Path = utils.init_path(path)
        self.objs: dict[int, Item] = {}

        self.img_type: type[Item] = img_type
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()

        utils.init_path(self.path / self.img_type.get_folder())

        json_utils.load_cards(self.path, self.objs, img_type)

        self.list_parser: ListParser = ListParser(self.img_type)
        self.item_parser: CardParser | StillParser = self.img_type.get_parser()

        self.updateables: list[int] = []

    async def __aenter__(self) -> Downloader:
        self.list_parser.set_session(self.session)
        self.item_parser.set_session(self.session)

        return self

    async def __aexit__(self, type: None, value: None, trace: None) -> None:
        await self.session.close()

    async def request_from_server(self, dest: Path, url: str) -> None:
        res: aiohttp.ClientResponse = await self.session.get(f"https:{url}")
        if res.status == 200:
            res_data: bytes = await res.read()
            with open(dest, 'wb') as f:
                f.write(res_data)

    async def download_file(self, path: Path, item: Item, i: int) -> None:
        if not path.exists() or item.key in self.updateables:
            await self.request_from_server(path, item.get_urls()[i])

            message: str = f"Downloaded item {item.key}"
            if isinstance(item, Card):
                message += f", {'idolized' if i == 1 else 'normal'}"
            message += "."

            print(message)

    async def update_if_needed(self, item: Item) -> None:
        if item.needs_update():
            _, updated_item = await self.item_parser.get_item(item.key)

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
        res: list[None] = await asyncio.gather(*tasks, return_exceptions=True)
        return res

    async def get_cards_from_parser(self) -> None:
        num_pages: int = await self.list_parser.get_num_pages()+1
        current_num: int = 1
        for _ in range(1, num_pages):
            current_page: list[None] = await self.get_page(current_num)
            if not current_page:
                break
            current_num += 1

    async def get_images(self, item: Item) -> None:
        paths: list[Path] = item.get_paths(self.path)
        try:
            for i, path in enumerate(paths):
                await self.download_file(path, item, i)
        except Exception as e:
            print(f"Couldn't download card {item.key}: {e}.")

    async def get(self) -> None:
        tasks: list[Coroutine] = []
        for _, item in self.objs.items():
            tasks.append(self.get_images(item))
        await asyncio.gather(*tasks, return_exceptions=False)

    async def update(self) -> None:
        print("Searching for new or missing items...")
        await self.get_cards_from_parser()

        print("Checking if items can be updated to better resolution...")
        for _, item in self.objs.items():
            await self.update_if_needed(item)

        self.update_json_file()
        print("Updated items database.")

    def update_json_file(self) -> None:
        self.objs = dict(
            sorted(self.objs.items(), reverse=True))
        json_utils.dump_to_file(json_utils.to_json(
            self.objs), self.path, self.img_type)
