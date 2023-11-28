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


import asyncio

from aiohttp import ClientResponse, ClientSession

import mikan.plugins


class ParsingError(Exception):
    pass


class Parser:
    def __init__(self, objs: dict[str, dict[str, list[str]]], img_type: str, session: ClientSession) -> None:
        self.session: ClientSession = session
        self.objs = objs
        self.card_type = mikan.plugins.registry[img_type]

        self.list_parser, self.item_parser = self.card_type.ListParser(), self.card_type.ItemParser()

    async def get(self, url: str) -> ClientResponse:
        return await self.session.get(url)

    async def get_page(self, idx: int) -> list[None]:
        data = await self.get(f"{self.card_type.list_url}{idx}") if not self.card_type.is_api else idx
        page = await self.list_parser.get_page(data)

        if self.card_type.card_dir not in self.objs:
            self.objs[self.card_type.card_dir] = {}

        tasks = [self.add_to_objs(item) for item in page if str(item) not in self.objs[self.card_type.card_dir]]

        res: list[None] = await asyncio.gather(*tasks, return_exceptions=False)

        return res

    async def get_items(self) -> None:
        num_pages = await self.list_parser.get_num_pages(await self.get(self.card_type.list_url)) + 1
        current_num = 1
        for _ in range(1, num_pages):
            current_page = await self.get_page(current_num)
            if not current_page and not self.card_type.is_api:
                break

            current_num += 1

    async def add_to_objs(self, item: int) -> None:
        obj = await self.item_parser.create_item(await self.get(f"{self.card_type.url}{item}"))
        self.objs[self.card_type.card_dir][str(item)] = obj
        print(f"Getting item {item}.")
