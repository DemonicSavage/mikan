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


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_downloader_cards(mocker, cleanup):
    downloader = mikan.downloader.Downloader(
        Path("test/temp"), Path("test/temp"), mikan.classes.Card
    )

    mocker.patch(
        "mikan.html_parser.ListParser.get_num_pages",
        return_value=test.mocks.mock_num_pages,
    )
    mocker.patch(
        "mikan.html_parser.ListParser.get_page",
        test.mocks.mock_page,
    )
    mocker.patch(
        "mikan.html_parser.CardParser.get_item",
        test.mocks.mock_card,
    )
    mocker.patch(
        "aiohttp.ClientSession.get", return_value=awaitable_res(test.mocks.mock_file)
    )

    async with downloader as downloader:
        await downloader.update()
        await downloader.get()

    assert (
        json.loads(Path("test/temp/items.json").open().read())["SIFAS_Cards"]
        == json.loads(test.mocks.cards_json)["SIFAS_Cards"]
    )
    assert check_files("test/temp/SIFAS_Cards", test.mocks.card_files)


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_downloader_sif_cards(mocker, cleanup):
    downloader = mikan.downloader.Downloader(
        Path("test/temp"), Path("test/temp"), mikan.classes.SIFCard
    )

    mocker.patch(
        "mikan.html_parser.SIFListParser.get_num_pages",
        return_value=test.mocks.mock_num_pages,
    )
    mocker.patch(
        "mikan.html_parser.SIFListParser.get_page",
        test.mocks.mock_page,
    )
    mocker.patch(
        "mikan.html_parser.SIFCardParser.get_item",
        test.mocks.mock_card,
    )
    mocker.patch(
        "aiohttp.ClientSession.get", return_value=awaitable_res(test.mocks.mock_file)
    )

    async with downloader as downloader:
        await downloader.update()
        await downloader.get()

    assert (
        json.loads(Path("test/temp/items.json").open().read())["SIF_Cards"]
        == json.loads(test.mocks.cards_json)["SIF_Cards"]
    )
    assert check_files("test/temp/SIF_Cards", test.mocks.card_files)


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_downloader_stills(mocker):
    downloader = mikan.downloader.Downloader(
        Path("test/temp"), Path("test/temp"), mikan.classes.Still
    )

    mocker.patch(
        "mikan.html_parser.ListParser.get_num_pages",
        return_value=test.mocks.mock_num_pages,
    )
    mocker.patch(
        "mikan.html_parser.ListParser.get_page",
        test.mocks.mock_page,
    )
    mocker.patch(
        "mikan.html_parser.StillParser.get_item",
        test.mocks.mock_still,
    )
    mocker.patch(
        "aiohttp.ClientSession.get", return_value=awaitable_res(test.mocks.mock_file)
    )

    async with downloader as downloader:
        await downloader.update()
        await downloader.get()

    assert (
        json.loads(Path("test/temp/items.json").open().read())["SIFAS_Stills"]
        == json.loads(test.mocks.cards_json)["SIFAS_Stills"]
    )
    assert check_files("test/temp/SIFAS_Stills", test.mocks.still_files)


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_downloader_fail(mocker):
    downloader = mikan.downloader.Downloader(
        Path("test/temp"), Path("test/temp"), mikan.classes.Card
    )

    mocker.patch(
        "mikan.html_parser.ListParser.get_num_pages",
        return_value=test.mocks.mock_num_pages,
    )
    mocker.patch(
        "mikan.html_parser.ListParser.get_page",
        test.mocks.mock_page,
    )
    mocker.patch(
        "mikan.html_parser.CardParser.get_item",
        test.mocks.mock_card,
    )
    mocker.patch("aiohttp.ClientSession.get", side_effect=aiohttp.ClientError("Err"))

    async with downloader as downloader:
        await downloader.update()
        await downloader.get()

    assert not Path("test/temp/SIFAS_Cards").exists()


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_downloader_card_load(mocker):
    directory = Path("test/temp")
    directory.mkdir(parents=True)
    with open(directory / "items.json", "w") as file:
        file.write(test.mocks.pre_json)
    downloader = mikan.downloader.Downloader(directory, directory, mikan.classes.Card)
    assert set(downloader.objs.keys()) == set(["SIFAS_Cards"])
