# Copyright (C) 2022-2023 DemonicSavage
# This file is part of Mikan.

# Mikan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.

# Mikan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Coroutine

import aiohttp
from tqdm.asyncio import tqdm

import mikan.html_parser as parser
from mikan import json_utils
from mikan.classes import Card, Item, SIFCard


class Downloader:
    def __init__(self, path: Path, img_type: type[Item]):
        self.path = path.expanduser()
        self.objs: dict[int, Item] = {}

        self.img_type = img_type

        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=None))

        json_utils.load_cards(self.path, self.objs, self.img_type)

        self.list_parser: parser.ListParser | parser.SIFListParser = (
            parser.ListParser(self.img_type)
            if self.img_type != SIFCard
            else parser.SIFListParser()
        )
        self.item_parser = getattr(parser, f"{img_type.__name__}Parser")()

        self.updateables: list[int] = []

    async def __aenter__(self) -> Downloader:
        self.list_parser.set_session(self.session)
        self.item_parser.set_session(self.session)

        return self

    async def __aexit__(self, ext_type: None, value: None, trace: None) -> None:
        await self.session.close()

    async def request_from_server(self, dest: Path, url: str) -> None:
        res = await self.session.get(f"https:{url}")

        if res.status == 200:
            res_data = await res.read()
            dest.parent.mkdir(exist_ok=True, parents=True)

            with open(dest, "wb") as file:
                file.write(res_data)

    async def download_file(self, path: Path, item: Item, i: int) -> None:
        try:
            await self.request_from_server(path, item.get_urls()[i])

            message = f"Downloaded item {item.key}"
            if isinstance(item, Card):
                message += f", {'idolized' if i == 1 else 'normal'}"
            message += "."

        except aiohttp.ClientError as e:
            message = f"Couldn't download item {item.key}: {e}"

        tqdm.write(message)

    async def update_if_needed(self, item: Item) -> None:
        if item.needs_update():
            _, updated_item = await self.item_parser.get_item(item.key)

            if item.get_urls()[0] != updated_item.get_urls()[0]:
                self.updateables.append(item.key)

            for i in range(len(item.get_urls())):
                item.set_url(i, updated_item.get_urls()[i])

    async def add_item_to_object_list(self, item: int) -> None:
        i, obj = await self.item_parser.get_item(item)
        self.objs[i] = obj
        print(f"Getting item {i}.")

    async def get_page(self, idx: int) -> list[None]:
        tasks: list[Coroutine[Any, Any, None]] = []
        page = await self.list_parser.get_page(idx)

        for item in page:
            if item not in self.objs:
                tasks.append(self.add_item_to_object_list(item))

        res: list[None] = await asyncio.gather(*tasks, return_exceptions=False)

        return res

    async def get_cards_from_parser(self) -> None:
        num_pages = await self.list_parser.get_num_pages() + 1
        current_num = 1
        for _ in range(1, num_pages):
            current_page = await self.get_page(current_num)
            if not current_page and self.img_type != SIFCard:
                break

            current_num += 1

    async def get(self) -> None:
        tasks: list[Coroutine[Any, Any, None]] = []

        for _, item in self.objs.items():
            paths = item.get_paths(self.path)
            tasks.extend(
                [
                    self.download_file(path, item, i)
                    for i, path in enumerate(paths)
                    if not path.exists() or item.key in self.updateables
                ]
            )

        await tqdm.gather(*tasks, disable=len(tasks) == 0)

    async def update(self) -> None:
        print("Searching for new or missing items...")
        await self.get_cards_from_parser()

        print("Checking if items can be updated to better resolution...")
        for _, item in self.objs.items():
            await self.update_if_needed(item)

        self.update_json_file()
        print("Updated items database.")

    def update_json_file(self) -> None:
        self.objs = dict(sorted(self.objs.items(), reverse=True))
        json_utils.dump_to_file(json_utils.to_json(self.objs), self.path, self.img_type)
