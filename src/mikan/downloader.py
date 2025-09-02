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
import mikan.plugins
from mikan import json_utils


class Downloader:
    def __init__(self, data_path: Path, config_path: Path, img_type: str, session: aiohttp.ClientSession):
        self.card_type = mikan.plugins.registry[img_type]

        self.path = data_path.expanduser() / self.card_type.card_dir
        self.config_path = config_path

        self.session = session

        self.objs = json_utils.load_cards(self.config_path)
        self.parser = parser.Parser(self.objs, img_type, self.session)

    async def download_file(self, item: str) -> None:
        try:
            if not item.startswith("https"):
                item = "https:" + item
            res = await self.session.get(item)
            if res.status == aiohttp.web.HTTPOk.status_code:
                self.path.mkdir(exist_ok=True, parents=True)

                item_name = self.card_type.item_renamer_fn(item)

                with open(self.path / item_name, "wb") as file:
                    async for chunk in res.content.iter_any():
                        file.write(chunk)

                message = f"Downloaded item {item_name}."
            else:
                message = f"Failed to download item {item}: HTTP status {res.status}"

        except aiohttp.ClientError as e:
            message = f"Couldn't download item {item}: {e}"

        tqdm.write(message)

    async def get_missing_items(self) -> None:
        tasks: list[Coroutine[Any, Any, None]] = [
            self.download_file(card)
            for item in self.objs[self.card_type.card_dir].values()
            for card in item
            if not (self.path / self.card_type.item_renamer_fn(card)).exists()
        ]

        await tqdm.gather(*tasks, disable=len(tasks) == 0)

    async def update(self) -> None:
        try:
            print("Searching for new or missing items...")
            await self.parser.get_items()

            self.update_json_file()
            print("Updated items database.")
        except Exception as e:
            print(f"An error occurred while updating items: {e}")

    def update_json_file(self) -> None:
        try:
            self.objs[self.card_type.card_dir] = dict(sorted(self.objs[self.card_type.card_dir].items(), reverse=True))
            json_utils.dump_to_file(self.objs, self.config_path)
        except Exception as e:
            print(f"An error occurred while updating the JSON file: {e}")
