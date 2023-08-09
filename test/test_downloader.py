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
import test.mocks
from pathlib import Path
from test.utils import awaitable_res

import aiohttp
import pytest

import mikan.classes
import mikan.downloader


def check_files(path, answer):
    path = Path(path)
    if not path.is_dir():
        return False
    files = [x.name for x in path.iterdir()]
    return set(files) == set(answer)


class MockConfig:
    cookie = ""
    data_dir = ""
    max_conn = 1


card_types = [
    (mikan.classes.Card, "SIFAS_Cards", test.mocks.card_files),
    (mikan.classes.SIFCard, "SIF_Cards", test.mocks.card_files),
    (mikan.classes.Still, "SIFAS_Stills", test.mocks.still_files),
]


@pytest.mark.parametrize("card_class, card_key, card_mock", card_types)
@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_downloader_cards(mocker, card_class, card_key, card_mock):
    downloader = mikan.downloader.Downloader(
        Path("test/temp"), Path("test/temp"), card_class, MockConfig()
    )
    mocker.patch(
        "mikan.html_parser.Parser.get_cards_from_pages",
        test.mocks.mock_get_items,
    )
    mocker.patch(
        "aiohttp.ClientSession.get", return_value=awaitable_res(test.mocks.mock_file)
    )

    async with downloader as downloader:
        downloader.objs = test.mocks.mock_objs
        await downloader.update()
        await downloader.get()

    assert (
        json.loads(Path("test/temp/items.json").open().read())[card_key]
        == json.loads(test.mocks.cards_json)[card_key]
    )
    assert check_files(f"test/temp/{card_key}", card_mock)


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_downloader_fail(mocker):
    downloader = mikan.downloader.Downloader(
        Path("test/temp"), Path("test/temp"), mikan.classes.Card, MockConfig()
    )

    mocker.patch(
        "mikan.html_parser.Parser.get_cards_from_pages",
        test.mocks.mock_get_items,
    )
    mocker.patch("aiohttp.ClientSession.get", side_effect=aiohttp.ClientError("Err"))

    async with downloader as downloader:
        downloader.objs = test.mocks.mock_objs
        await downloader.update()
        await downloader.get()

    assert not Path("test/temp/SIFAS_Cards").exists()


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_downloader_card_load():
    directory = Path("test/temp")
    directory.mkdir(parents=True)
    with open(directory / "items.json", "w") as file:
        file.write(test.mocks.pre_json)
    downloader = mikan.downloader.Downloader(
        directory, directory, mikan.classes.Card, MockConfig()
    )
    assert set(downloader.objs.keys()) == set(["SIFAS_Cards"])
