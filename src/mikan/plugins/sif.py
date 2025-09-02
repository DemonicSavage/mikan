#!/usr/bin/env python3
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

from typing import Any

from aiohttp import ClientResponse

from mikan.plugins.default import DefaultPlugin


class SIF(DefaultPlugin):
    card_dir = "SIF_Cards"
    url = "https://schoolido.lu/api/cards/"
    list_url = "https://schoolido.lu/api/cardids/"
    cli_arg = "sif"
    desc = "SIF cards"
    is_api = True

    class ListParser:
        def __init__(self) -> None:
            self.items: list[list[int]] = []

        async def get_page(self, num: Any) -> list[int]:  # NOSONAR(S7503)
            return self.items[num - 1]

        async def get_num_pages(self, data: ClientResponse) -> int:
            json = await data.json()
            self.items = [json[i : i + 10] for i in range(0, len(json), 10)]
            return len(self.items)

    class ItemParser:
        async def create_item(self, data: ClientResponse) -> list[str]:
            json = await data.json()
            return [card for card in [json["card_image"], json["card_idolized_image"]] if card]
