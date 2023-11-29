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

import json
from test.utils import MockResponse

cards_json = """{
    "SIFAS_Stills": {
        "6": ["//url6.png"],
        "5": ["//url5.png"],
        "4": ["//url4.png"],
        "3": ["//url3.png"],
        "2": ["//url2.png"],
        "1": ["//url1.png"]
    }
}"""

still_files = [
    "url1.png",
    "url2.png",
    "url3.png",
    "url4.png",
    "url5.png",
    "url6.png",
]


mock_num_pages = 3


async def mock_get_items(*_):
    pass


mock_objs = json.loads(cards_json)


mock_file = MockResponse(
    bytes(0x2A),
    200,
)

mock_empty_response = MockResponse("", 200)

pre_json = """{
    "SIFAS_Stills": {
        "4": ["//url4.png"]
    }
    }"""
