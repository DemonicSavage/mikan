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

import mikan.html_parser
from mikan.main import discover_plugins

discover_plugins()


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
    (mikan.plugins.sif.SIF.ListParser, test.mocks.mock_sif_list_response, 1),
    (mikan.plugins.sifas.SIFAS.ListParser, test.mocks.mock_list_response, 42),
]

list_num_pages_types = [
    (mikan.plugins.sif.SIF.ListParser, test.mocks.mock_sif_list_response, 1),
    (mikan.plugins.sifas.SIFAS.ListParser, test.mocks.mock_num_pages_response, 42),
]

card_types = [
    (
        mikan.plugins.sifas.SIFAS.ItemParser,
        test.mocks.mock_card_response,
        ["98Normal", "98Idolized"],
    ),
    (
        mikan.plugins.sif.SIF.ItemParser,
        test.mocks.mock_sif_card_response,
        ["Normal", "Idolized"],
    ),
    (
        mikan.plugins.sifasstills.SIFASStills.ItemParser,
        test.mocks.mock_still_response,
        ["98Still"],
    ),
]

card_error_types = [
    (mikan.plugins.sifas.SIFAS.ItemParser, test.mocks.mock_card_response_error),
    (mikan.plugins.sifasstills.SIFASStills.ItemParser, test.mocks.mock_still_response_error),
]


@pytest.mark.asyncio()
async def test_parser(mocker):
    parser = mikan.html_parser.Parser({"SIFAS_Cards": {}}, "SIFAS", aiohttp.ClientSession())
    mocker.patch(
        "mikan.plugins.sifas.SIFAS.ItemParser.create_item",
        return_value=["//normal1.png", "//idolized1.png"],
    )
    mocker.patch("mikan.plugins.sifas.SIFAS.ListParser.get_num_pages", return_value=2),
    mocker.patch("mikan.plugins.sifas.SIFAS.ListParser.get_page", return_value=[1]),
    mocker.patch("aiohttp.ClientSession.get", test.mocks.mock_get_items)
    parser.objs = {}
    await parser.get_items()
    await parser.session.close()
    assert parser.objs["SIFAS_Cards"] == {"1": ["//normal1.png", "//idolized1.png"]}


@pytest.mark.asyncio()
async def test_list_parser():
    async with Parser(mikan.plugins.sifas.SIFAS.ListParser()) as parser:
        assert await parser.parser.get_page(test.mocks.mock_list_response) == [123]


@pytest.mark.asyncio()
async def test_sif_list_parser():
    async with Parser(mikan.plugins.sif.SIF.ListParser()) as parser:
        await parser.parser.get_num_pages(test.mocks.mock_sif_list_response)
        assert await parser.parser.get_page(1) == [123]


@pytest.mark.parametrize(("list_parser", "list_mock", "list_res"), list_num_pages_types)
@pytest.mark.asyncio()
async def test_num_pages_parser(list_parser, list_mock, list_res):
    async with Parser(list_parser()) as parser:
        assert await parser.parser.get_num_pages(list_mock) == list_res


@pytest.mark.parametrize(("card_parser", "card_mock", "card_res"), card_types)
@pytest.mark.asyncio()
async def test_sif_card_parser(card_parser, card_mock, card_res):
    async with Parser(card_parser()) as parser:
        assert await parser.parser.create_item(card_mock) == card_res


@pytest.mark.asyncio()
async def test_list_parser_fail():
    async with Parser(mikan.plugins.sifas.SIFAS.ListParser()) as parser:
        with pytest.raises(mikan.html_parser.ParsingError) as ex:
            await parser.parser.get_page(test.mocks.mock_list_response_error)
        assert ex.type == mikan.html_parser.ParsingError


@pytest.mark.asyncio()
async def test_num_pages_parser_fail():
    async with Parser(mikan.plugins.sifas.SIFAS.ListParser()) as parser:
        with pytest.raises(mikan.html_parser.ParsingError) as ex:
            await parser.parser.get_num_pages(test.mocks.mock_num_pages_response_error)
        assert ex.type == mikan.html_parser.ParsingError


@pytest.mark.parametrize(("card_parser", "card_mock"), card_error_types)
@pytest.mark.asyncio()
async def test_card_parser_fail(card_parser, card_mock):
    async with Parser(card_parser()) as parser:
        with pytest.raises(mikan.html_parser.ParsingError) as ex:
            await parser.parser.create_item(card_mock)
    assert ex.type == mikan.html_parser.ParsingError
