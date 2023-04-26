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
from test.utils import awaitable_res

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


@pytest.mark.asyncio
async def test_list_parser(mocker):
    async with Parser(mikan.html_parser.ListParser()) as parser:
        assert await parser.parser.get_page(test.mocks.mock_list_response) == [123]


@pytest.mark.asyncio
async def test_sif_list_parser(mocker):
    async with Parser(mikan.html_parser.SIFListParser()) as parser:
        await parser.parser.get_num_pages(test.mocks.mock_sif_list_response)
        assert await parser.parser.get_page(1) == [123]


@pytest.mark.asyncio
async def test_sif_num_pages_parser(mocker):
    async with Parser(mikan.html_parser.SIFListParser()) as parser:
        assert await parser.parser.get_num_pages(test.mocks.mock_sif_list_response) == 1


@pytest.mark.asyncio
async def test_num_pages_parser(mocker):
    async with Parser(mikan.html_parser.ListParser()) as parser:
        assert (
            await parser.parser.get_num_pages(test.mocks.mock_num_pages_response) == 42
        )


@pytest.mark.asyncio
async def test_sif_card_parser(mocker):
    async with Parser(mikan.html_parser.SIFCardParser()) as parser:
        assert await parser.parser.create_item(test.mocks.mock_sif_card_response) == (
            "98",
            ["Normal", "Idolized"],
        )


@pytest.mark.asyncio
async def test_card_parser(mocker):
    async with Parser(mikan.html_parser.CardParser()) as parser:
        assert await parser.parser.create_item(test.mocks.mock_card_response) == (
            "98",
            ["98Normal", "98Idolized"],
        )


@pytest.mark.asyncio
async def test_still_parser(mocker):
    mocker.patch(
        "mikan.html_parser.aiohttp.ClientSession.get",
        return_value=awaitable_res(test.mocks.mock_still_response),
    )
    async with Parser(mikan.html_parser.StillParser()) as parser:
        assert await parser.parser.create_item(test.mocks.mock_still_response) == (
            "98",
            ["98URL"],
        )


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


@pytest.mark.asyncio
async def test_card_parser_fail(mocker):
    async with Parser(mikan.html_parser.CardParser()) as parser:
        with pytest.raises(mikan.html_parser.ItemParsingException) as ex:
            await parser.parser.create_item(test.mocks.mock_card_response_error)
    assert ex.type == mikan.html_parser.ItemParsingException


@pytest.mark.asyncio
async def test_still_parser_fail(mocker):
    async with Parser(mikan.html_parser.StillParser()) as parser:
        with pytest.raises(mikan.html_parser.ItemParsingException) as ex:
            await parser.parser.create_item(test.mocks.mock_still_response_error)
    assert ex.type == mikan.html_parser.ItemParsingException
