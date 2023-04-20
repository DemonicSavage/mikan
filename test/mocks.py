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

import mikan.classes

cards_json = """{
    "6": {
        "key": 6,
        "idol": "Name6",
        "rarity": "Rarity6",
        "attribute": "Attribute6",
        "unit": "Unit6",
        "subunit": "Subunit6",
        "year": "Year6",
        "normal_url": "//normal6.png",
        "idolized_url": "//idolized6.png"
    },
    "5": {
        "key": 5,
        "idol": "Name5",
        "rarity": "Rarity5",
        "attribute": "Attribute5",
        "unit": "Unit5",
        "subunit": "Subunit5",
        "year": "Year5",
        "normal_url": "//normal5.png",
        "idolized_url": "//idolized5.png"
    },
    "4": {
        "key": 4,
        "idol": "Name4",
        "rarity": "Rarity4",
        "attribute": "Attribute4",
        "unit": "Unit4",
        "subunit": "Subunit4",
        "year": "Year4",
        "normal_url": "//normal4.png",
        "idolized_url": "//idolized4.png"
    },
    "3": {
        "key": 3,
        "idol": "Name3",
        "rarity": "Rarity3",
        "attribute": "Attribute3",
        "unit": "Unit3",
        "subunit": "Subunit3",
        "year": "Year3",
        "normal_url": "//normal3.png",
        "idolized_url": "//idolized3.png"
    },
    "2": {
        "key": 2,
        "idol": "Name2",
        "rarity": "Rarity2",
        "attribute": "Attribute2",
        "unit": "Unit2",
        "subunit": "Subunit2",
        "year": "Year2",
        "normal_url": "//normal2.png",
        "idolized_url": "//idolized2.png"
    },
    "1": {
        "key": 1,
        "idol": "Name1",
        "rarity": "Rarity1",
        "attribute": "Attribute1",
        "unit": "Unit1",
        "subunit": "Subunit1",
        "year": "Year1",
        "normal_url": "//normal1.png",
        "idolized_url": "//idolized1.png"
    }
}"""

stills_json = """{
    "6": {
        "key": 6,
        "url": "//url6.png"
    },
    "5": {
        "key": 5,
        "url": "//url5.png"
    },
    "4": {
        "key": 4,
        "url": "//url4.png"
    },
    "3": {
        "key": 3,
        "url": "//url3.png"
    },
    "2": {
        "key": 2,
        "url": "//url2.png"
    },
    "1": {
        "key": 1,
        "url": "//url1.png"
    }
}"""

card_files = [
    "1_Unit1_Name1_Idolized.png",
    "1_Unit1_Name1_Normal.png",
    "2_Unit2_Name2_Idolized.png",
    "2_Unit2_Name2_Normal.png",
    "3_Unit3_Name3_Idolized.png",
    "3_Unit3_Name3_Normal.png",
    "4_Unit4_Name4_Idolized.png",
    "4_Unit4_Name4_Normal.png",
    "5_Unit5_Name5_Idolized.png",
    "5_Unit5_Name5_Normal.png",
    "6_Unit6_Name6_Idolized.png",
    "6_Unit6_Name6_Normal.png",
]

sif_card_files = [
    "1_Name1_Idolized.png",
    "1_Name1_Normal.png",
    "2_Name2_Idolized.png",
    "2_Name2_Normal.png",
    "3_Name3_Idolized.png",
    "3_Name3_Normal.png",
    "4_Name4_Idolized.png",
    "4_Name4_Normal.png",
    "5_Name5_Idolized.png",
    "5_Name5_Normal.png",
    "6_Name6_Idolized.png",
    "6_Name6_Normal.png",
]

still_files = [
    "1_Still.png",
    "2_Still.png",
    "3_Still.png",
    "4_Still.png",
    "5_Still.png",
    "6_Still.png",
]

mock_num_pages = 3


async def mock_page(self, n):
    return [[1, 2, 3], [4, 5, 6], []][n - 1]


async def mock_card(self, n):
    return n, mikan.classes.Card(
        n,
        f"Name{n}",
        f"Rarity{n}",
        f"Attribute{n}",
        f"Unit{n}",
        f"Subunit{n}",
        f"Year{n}",
        f"//normal{n}.png",
        f"//idolized{n}.png",
    )


async def mock_sif_card(self, n):
    return n, mikan.classes.SIFCard(
        n,
        f"Name{n}",
        f"Rarity{n}",
        f"Attribute{n}",
        f"Unit{n}",
        f"Subunit{n}",
        f"Year{n}",
        f"//normal{n}.png",
        f"//idolized{n}.png",
    )


async def mock_still(self, n):
    return n, mikan.classes.Still(
        n,
        f"//url{n}.png",
    )


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
    <a href="Normal"></a>
    <a href="Idolized"></a>
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
        <a href='URL'></a>
    </div>
    """,
    200,
)

mock_still_response_error = MockResponse(
    mock_still_response._text.replace("top-item", "top-tem"), 200
)
mock_card_response_error = MockResponse(
    mock_card_response._text.replace("top-item", "top-tem"), 200
)
mock_list_response_error = MockResponse(
    mock_list_response._text.replace("top-item", "top-tem"), 200
)
mock_num_pages_response_error = MockResponse(
    mock_list_response._text.replace("pagination", "paginaion"), 200
)
mock_card_response_data_error = MockResponse(
    mock_card_response._text.replace("idol", "idl"), 200
)

pre_json = """{
        "4": {
        "key": 4,
        "idol": "Name4",
        "rarity": "Rarity4",
        "attribute": "Attribute4",
        "unit": "Unit4",
        "subunit": "Subunit4",
        "year": "Year4",
        "normal_url": "//normal4.png",
        "idolized_url": "//idolized4.png"
        }
    }"""
