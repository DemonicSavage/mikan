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
from mikan.plugins import registry
import pytest
from unittest.mock import MagicMock


class Parser:
    def __init__(self, parser):
        self.parser = parser

    async def __aenter__(self):
        self.parser.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, a, b, c):
        if self.parser.session:
            await self.parser.session.close()


@pytest.mark.asyncio()
async def test_parser(mocker):
    registry["MockPlugin"] = test.mocks.MockPlugin()
    parser = mikan.html_parser.Parser({"Mock": {}}, "MockPlugin", aiohttp.ClientSession())
    mocker.patch("aiohttp.ClientSession.get", test.mocks.mock_get_items)
    parser.objs = {}
    await parser.get_items()
    await parser.session.close()
    assert parser.objs["Mock"] == {"1": ["//not_a_real_url/item/1/item.png"]}


@pytest.mark.asyncio
async def test_get_page_exception(mocker):
    parser = mikan.html_parser.Parser({}, "MockPlugin", aiohttp.ClientSession())
    mocker.patch("aiohttp.ClientSession.get", test.mocks.mock_get_items)
    mocker.patch("test.mocks.MockPlugin.ListParser.get_page", side_effect=mikan.html_parser.ParsingError())
    result = await parser.get_page("https://example.com")
    assert result == []


@pytest.mark.asyncio
async def test_get_items_exception(mocker):
    parser = mikan.html_parser.Parser({}, "MockPlugin", aiohttp.ClientSession())
    mocker.patch("aiohttp.ClientSession.get", test.mocks.mock_get_items)
    spy = mocker.spy(parser, "get_page")
    mocker.patch("test.mocks.MockPlugin.ListParser.get_num_pages", side_effect=mikan.html_parser.ParsingError())
    await parser.get_items()
    spy.assert_not_called()


@pytest.mark.asyncio
async def test_add_to_objs_exception(mocker):
    parser = mikan.html_parser.Parser({}, "MockPlugin", aiohttp.ClientSession())
    mocker.patch("aiohttp.ClientSession.get", test.mocks.mock_get_items)
    mocker.patch("test.mocks.MockPlugin.ItemParser.create_item", side_effect=mikan.html_parser.ParsingError())
    await parser.add_to_objs(1)
    assert parser.objs == {}
