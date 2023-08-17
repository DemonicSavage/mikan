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


async def mock_get_items(self, _=None):
    pass


mock_objs = json.loads(cards_json)


mock_file = MockResponse(
    bytes(0x2A),
    200,
)

mock_list_response = MockResponse(
    """
    <div class='top-item'>
        <a href='/123/'></a>
    </div>
    """,
    200,
)
mock_sif_list_response = MockResponse(
    """
    [123]
    """,
    200,
)


async def mock_sif_list_json():
    return json.loads(await mock_sif_list_response.text())


mock_sif_card_response = MockResponse(
    """{
        "idol": {"name": "Name", "main_unit": "Unit", "sub_unit": "Subunit", "year": "Year"},
        "rarity": "Rarity",
        "attribute": "Attribute",
        "card_image": "Normal",
        "card_idolized_image": "Idolized",
        "id": 98
        }""",
    200,
)


async def mock_sif_card_json():
    return json.loads(await mock_sif_card_response.text())


mock_sif_list_response.json = mock_sif_list_json
mock_sif_card_response.json = mock_sif_card_json

mock_num_pages_response = MockResponse(
    """
    <div class='pagination'>
        <a href='=1'></a>
        <a href='=42'></a>
        <a href='last'></a>
    </div>
    """,
    200,
)
mock_card_response = MockResponse(
    """
    <div class="top-item">
    <a href="98Normal"></a>
    <a href="98Idolized"></a>
    </div>

    <div>
    <div data-field="idol">
    null\nName
    </div>
    <div data-field="rarity">
    null\nRarity
    </div>
    <div data-field="attribute">
    null\nAttribute
    </div>
    <div data-field="idol__i_unit">
    null\nUnit
    </div>
    <div data-field="idol__i_subunit">
    null\nSubunit
    </div>
    <div data-field="idol__i_year">
    null\nYear
    </div>
    </div>
    """,
    200,
)
mock_still_response = MockResponse(
    """
    <div class='top-item'>
        <a href='98Still'></a>
    </div>
    """,
    200,
)

mock_still_response_error = MockResponse(mock_still_response._text.replace("top-item", "top-tem"), 200)
mock_card_response_error = MockResponse(mock_card_response._text.replace("top-item", "top-tem"), 200)
mock_list_response_error = MockResponse(mock_list_response._text.replace("top-item", "top-tem"), 200)
mock_num_pages_response_error = MockResponse(mock_list_response._text.replace("pagination", "paginaion"), 200)
mock_card_response_data_error = MockResponse(mock_card_response._text.replace("idol", "idl"), 200)

pre_json = """{
    "SIFAS_Cards": {
        "4": ["//normal4.png", "//idolized4.png"]
    }
    }"""
