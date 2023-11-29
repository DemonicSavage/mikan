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
    "SIFAS_Cards": {
        "6": ["//normal6.png", "//idolized6.png"],
        "5": ["//normal5.png", "//idolized5.png"],
        "4": ["//normal4.png", "//idolized4.png"],
        "3": ["//normal3.png", "//idolized3.png"],
        "2": ["//normal2.png", "//idolized2.png"],
        "1": ["//normal1.png", "//idolized1.png"]
    },
    "SIFAS_Stills": {
        "6": ["//url6.png"],
        "5": ["//url5.png"],
        "4": ["//url4.png"],
        "3": ["//url3.png"],
        "2": ["//url2.png"],
        "1": ["//url1.png"]
    },
    "SIF_Cards": {
        "6": ["//normal6.png", "//idolized6.png"],
        "5": ["//normal5.png", "//idolized5.png"],
        "4": ["//normal4.png", "//idolized4.png"],
        "3": ["//normal3.png", "//idolized3.png"],
        "2": ["//normal2.png", "//idolized2.png"],
        "1": ["//normal1.png", "//idolized1.png"]
    }
}"""

card_files = [
    "idolized1.png",
    "normal1.png",
    "idolized2.png",
    "normal2.png",
    "idolized3.png",
    "normal3.png",
    "idolized4.png",
    "normal4.png",
    "idolized5.png",
    "normal5.png",
    "idolized6.png",
    "normal6.png",
]

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
    "SIFAS_Cards": {
        "4": ["//normal4.png", "//idolized4.png"]
    }
    }"""
