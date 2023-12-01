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

from test.utils import MockResponse

from mikan.plugins.default import DefaultPlugin

cards_json = """{
    "Mock": {
        "1": ["//not_a_real_url/item/1/item.png"]
    }
}"""

card_files = [
    "item.png",
]


class MockPlugin:
    card_dir = "Mock"
    url = "https://not_a_real_url/item/"
    list_url = "https://not_a_real_url/items/?page="
    cli_arg = "mock"
    desc = "mocks"
    is_api = False

    @staticmethod
    def item_renamer_fn(_):
        return DefaultPlugin.item_renamer_fn(_)

    class ListParser:
        async def get_page(self, data) -> list[int]:
            return [1]

        async def get_num_pages(self, data) -> int:
            return 3

    class ItemParser:
        async def create_item(self, data) -> list[str]:
            return ["//not_a_real_url/item/1/item.png"]


async def mock_get_items(*_):
    pass


mock_file = MockResponse(
    bytes(0x2A),
    200,
)

mock_empty_response = MockResponse("", 200)
