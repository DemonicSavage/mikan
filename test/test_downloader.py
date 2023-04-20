# Copyright (C) 2022-2023 DemonicSavage
# This file is part of SIFAS Card Downloader.

# SIFAS Card Downloader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.

# SIFAS Card Downloader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License

import test.mocks
from pathlib import Path
from test.utils import awaitable_res

import aiohttp
import pytest

import sifas_card_downloader.classes
import sifas_card_downloader.downloader


def check_files(path, answer):
    path = Path(path)
    if not path.is_dir():
        return False
    files = [x.name for x in path.iterdir()]
    return set(files) == set(answer)


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_downloader_cards(mocker, cleanup):
    downloader = sifas_card_downloader.downloader.Downloader(
        Path("test/temp"), sifas_card_downloader.classes.Card
    )

    mocker.patch(
        "sifas_card_downloader.html_parser.ListParser.get_num_pages",
        return_value=test.mocks.mock_num_pages,
    )
    mocker.patch(
        "sifas_card_downloader.html_parser.ListParser.get_page",
        test.mocks.mock_page,
    )
    mocker.patch(
        "sifas_card_downloader.html_parser.CardParser.get_item",
        test.mocks.mock_card,
    )
    mocker.patch(
        "aiohttp.ClientSession.get", return_value=awaitable_res(test.mocks.mock_file)
    )

    async with downloader as downloader:
        await downloader.update()
        await downloader.get()

    assert Path("test/temp/sifas_cards.json").open().read() == test.mocks.cards_json
    assert check_files("test/temp/SIFAS_Cards", test.mocks.card_files)


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_downloader_sif_cards(mocker, cleanup):
    downloader = sifas_card_downloader.downloader.Downloader(
        Path("test/temp"), sifas_card_downloader.classes.SIFCard
    )

    mocker.patch(
        "sifas_card_downloader.html_parser.SIFListParser.get_num_pages",
        return_value=test.mocks.mock_num_pages,
    )
    mocker.patch(
        "sifas_card_downloader.html_parser.SIFListParser.get_page",
        test.mocks.mock_page,
    )
    mocker.patch(
        "sifas_card_downloader.html_parser.SIFCardParser.get_item",
        test.mocks.mock_sif_card,
    )
    mocker.patch(
        "aiohttp.ClientSession.get", return_value=awaitable_res(test.mocks.mock_file)
    )

    async with downloader as downloader:
        await downloader.update()
        await downloader.get()

    assert Path("test/temp/sif_cards.json").open().read() == test.mocks.cards_json
    assert check_files("test/temp/SIF_Cards", test.mocks.sif_card_files)


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_downloader_stills(mocker):
    downloader = sifas_card_downloader.downloader.Downloader(
        Path("test/temp"), sifas_card_downloader.classes.Still
    )

    mocker.patch(
        "sifas_card_downloader.html_parser.ListParser.get_num_pages",
        return_value=test.mocks.mock_num_pages,
    )
    mocker.patch(
        "sifas_card_downloader.html_parser.ListParser.get_page",
        test.mocks.mock_page,
    )
    mocker.patch(
        "sifas_card_downloader.html_parser.StillParser.get_item",
        test.mocks.mock_still,
    )
    mocker.patch(
        "aiohttp.ClientSession.get", return_value=awaitable_res(test.mocks.mock_file)
    )

    async with downloader as downloader:
        await downloader.update()
        await downloader.get()

    assert Path("test/temp/sifas_stills.json").open().read() == test.mocks.stills_json
    assert check_files("test/temp/SIFAS_Stills", test.mocks.still_files)


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_downloader_fail(mocker):
    downloader = sifas_card_downloader.downloader.Downloader(
        Path("test/temp"), sifas_card_downloader.classes.Card
    )

    mocker.patch(
        "sifas_card_downloader.html_parser.ListParser.get_num_pages",
        return_value=test.mocks.mock_num_pages,
    )
    mocker.patch(
        "sifas_card_downloader.html_parser.ListParser.get_page",
        test.mocks.mock_page,
    )
    mocker.patch(
        "sifas_card_downloader.html_parser.CardParser.get_item",
        test.mocks.mock_card,
    )
    mocker.patch("aiohttp.ClientSession.get", side_effect=aiohttp.ClientError("Err"))

    async with downloader as downloader:
        await downloader.update()
        await downloader.get()

    assert not Path("test/temp/SIFAS_Cards").exists()


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_downloader_update_2x(mocker):
    downloader = sifas_card_downloader.downloader.Downloader(
        Path("test/temp"), sifas_card_downloader.classes.Card
    )

    mocker.patch(
        "sifas_card_downloader.html_parser.CardParser.get_item",
        test.mocks.mock_card,
    )
    _, old_card = await test.mocks.mock_card(downloader, 2)
    old_card.normal_url = "old"

    async with downloader as downloader:
        await downloader.update_if_needed(old_card)

    assert downloader.updateables == [2]


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_downloader_card_load(mocker):
    directory = Path("test/temp")
    directory.mkdir(parents=True)
    with open(directory / "sifas_cards.json", "w") as file:
        file.write(test.mocks.pre_json)
    downloader = sifas_card_downloader.downloader.Downloader(
        directory, sifas_card_downloader.classes.Card
    )
    assert list(downloader.objs.keys()) == [4]
