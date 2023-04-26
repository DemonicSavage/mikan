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

import test.mocks

import aiohttp
import pytest

import mikan.classes
import mikan.html_parser


class Parser:
    def __init__(self, parser):
        self.parser = parser

    async def __aenter__(self):
        self.parser.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, a, b, c):
        if self.parser.session:
            await self.parser.session.close()


list_types = [
    (mikan.html_parser.SIFListParser, test.mocks.mock_sif_list_response, 1),
    (mikan.html_parser.ListParser, test.mocks.mock_list_response, 42),
]

list_num_pages_types = [
    (mikan.html_parser.SIFListParser, test.mocks.mock_sif_list_response, 1),
    (mikan.html_parser.ListParser, test.mocks.mock_num_pages_response, 42),
]

card_types = [
    (
        mikan.html_parser.CardParser,
        test.mocks.mock_card_response,
        ("98", ["98Normal", "98Idolized"]),
    ),
    (
        mikan.html_parser.SIFCardParser,
        test.mocks.mock_sif_card_response,
        ("98", ["Normal", "Idolized"]),
    ),
    (mikan.html_parser.StillParser, test.mocks.mock_still_response, ("98", ["98URL"])),
]

card_error_types = [
    (mikan.html_parser.CardParser, test.mocks.mock_card_response_error),
    (mikan.html_parser.StillParser, test.mocks.mock_still_response_error),
]


@pytest.mark.asyncio
async def test_list_parser(mocker):
    async with Parser(mikan.html_parser.ListParser()) as parser:
        assert await parser.parser.get_page(test.mocks.mock_list_response) == [123]


@pytest.mark.asyncio
async def test_sif_list_parser(mocker):
    async with Parser(mikan.html_parser.SIFListParser()) as parser:
        await parser.parser.get_num_pages(test.mocks.mock_sif_list_response)
        assert await parser.parser.get_page(1) == [123]


@pytest.mark.parametrize("list_parser, list_mock, list_res", list_num_pages_types)
@pytest.mark.asyncio
async def test_num_pages_parser(mocker, list_parser, list_mock, list_res):
    async with Parser(list_parser()) as parser:
        assert await parser.parser.get_num_pages(list_mock) == list_res


@pytest.mark.parametrize("card_parser, card_mock, card_res", card_types)
@pytest.mark.asyncio
async def test_sif_card_parser(mocker, card_parser, card_mock, card_res):
    async with Parser(card_parser()) as parser:
        assert await parser.parser.create_item(card_mock) == card_res


@pytest.mark.asyncio
async def test_list_parser_fail(mocker):
    async with Parser(mikan.html_parser.ListParser()) as parser:
        with pytest.raises(mikan.html_parser.ListParsingException) as ex:
            await parser.parser.get_page(test.mocks.mock_list_response_error)
        assert ex.type == mikan.html_parser.ListParsingException


@pytest.mark.asyncio
async def test_num_pages_parser_fail(mocker):
    async with Parser(mikan.html_parser.ListParser()) as parser:
        with pytest.raises(mikan.html_parser.ListParsingException) as ex:
            await parser.parser.get_num_pages(test.mocks.mock_num_pages_response_error)
        assert ex.type == mikan.html_parser.ListParsingException


@pytest.mark.parametrize("card_parser, card_mock", card_error_types)
@pytest.mark.asyncio
async def test_card_parser_fail(mocker, card_parser, card_mock):
    async with Parser(card_parser()) as parser:
        with pytest.raises(mikan.html_parser.ItemParsingException) as ex:
            await parser.parser.create_item(card_mock)
    assert ex.type == mikan.html_parser.ItemParsingException
