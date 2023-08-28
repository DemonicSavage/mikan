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

from pathlib import Path
from typing import Any, Coroutine

import aiohttp
import aiohttp.web
from tqdm.asyncio import tqdm

import mikan.html_parser as parser
from mikan import json_utils
from mikan.classes import CardType


class Downloader:
    def __init__(self, data_path: Path, config_path: Path, img_type: CardType, session: aiohttp.ClientSession):
        self.path = data_path.expanduser() / img_type.results_dir
        self.config_path = config_path

        self.img_type = img_type
        self.session = session

        self.objs = json_utils.load_cards(self.config_path)
        self.parser = parser.Parser(self.objs, self.img_type, self.session)

    async def download_file(self, item: str) -> None:
        try:
            res = await self.session.get(f"https:{item}")
            if res.status == aiohttp.web.HTTPOk.status_code:
                self.path.mkdir(exist_ok=True, parents=True)

                with open(self.path / self.get_name(item), "wb") as file:
                    async for chunk in res.content.iter_any():
                        file.write(chunk)

                message = f"Downloaded item {self.get_name(item)}."

        except aiohttp.ClientError as e:
            message = f"Couldn't download item {item}: {e}"

        tqdm.write(message)

    def get_name(self, url: str) -> str:
        return url.split("/")[-1]

    async def get(self) -> None:
        tasks: list[Coroutine[Any, Any, None]] = []

        for item in self.objs[self.img_type.results_dir].values():
            tasks.extend([self.download_file(card) for card in item if not (self.path / self.get_name(card)).exists()])

        await tqdm.gather(*tasks, disable=len(tasks) == 0)

    async def update(self) -> None:
        print("Searching for new or missing items...")
        await self.parser.get_items()

        self.update_json_file()
        print("Updated items database.")

    def update_json_file(self) -> None:
        self.objs[self.img_type.results_dir] = dict(sorted(self.objs[self.img_type.results_dir].items(), reverse=True))
        json_utils.dump_to_file(self.objs, self.config_path)
