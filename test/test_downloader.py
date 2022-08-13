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

    assert Path("test/temp/cards.json").open().read() == test.mocks.cards_json
    assert check_files("test/temp/All", test.mocks.card_files)


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

    assert Path("test/temp/stills.json").open().read() == test.mocks.stills_json
    assert check_files("test/temp/Stills", test.mocks.still_files)


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

    assert not Path("test/temp/All").exists()


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
    with open(directory / "cards.json", "w") as file:
        file.write(test.mocks.pre_json)
    downloader = sifas_card_downloader.downloader.Downloader(
        directory, sifas_card_downloader.classes.Card
    )
    assert list(downloader.objs.keys()) == [4]
