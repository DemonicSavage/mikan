from pathlib import Path
import shutil
import pytest

import src.downloader
import src.classes
import test.strings
from test.mocks import MockResponse, awaitable_res

num_pages = 3


async def mock_page(self, n):
    return [[1, 2, 3], [4, 5, 6], []][n - 1]


async def mock_card(self, n):
    return n, src.classes.Card(
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
    return n, src.classes.Still(
        n,
        f"//url{n}.png",
    )


mock_file = MockResponse(
    bytes(0x2A),
    200,
)


@pytest.mark.asyncio
async def test_downloader_cards(mocker):
    downloader = src.downloader.Downloader(Path("test/temp"), src.classes.Card)
    mocker.patch(
        "src.html_parser.ListParser.get_num_pages",
        return_value=num_pages,
    )
    mocker.patch(
        "src.html_parser.ListParser.get_page",
        mock_page,
    )
    mocker.patch(
        "src.html_parser.CardParser.get_item",
        mock_card,
    )
    mocker.patch("aiohttp.ClientSession.get", return_value=awaitable_res(mock_file))
    async with downloader as downloader:
        await downloader.update()
        await downloader.get()
        assert Path("test/temp/cards.json").open().read() == test.strings.cards_json
    shutil.rmtree("test/temp", ignore_errors=True)


@pytest.mark.asyncio
async def test_downloader_stills(mocker):
    downloader = src.downloader.Downloader(Path("test/temp"), src.classes.Still)
    mocker.patch(
        "src.html_parser.ListParser.get_num_pages",
        return_value=num_pages,
    )
    mocker.patch(
        "src.html_parser.ListParser.get_page",
        mock_page,
    )
    mocker.patch(
        "src.html_parser.StillParser.get_item",
        mock_still,
    )
    mocker.patch("aiohttp.ClientSession.get", return_value=awaitable_res(mock_file))
    async with downloader as downloader:
        await downloader.update()
        await downloader.get()
        assert Path("test/temp/stills.json").open().read() == test.strings.stills_json
    shutil.rmtree("test/temp", ignore_errors=True)
