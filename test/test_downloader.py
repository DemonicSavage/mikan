from pathlib import Path
import pytest

import src.downloader
import src.classes
import test.mocks
from test.utils import awaitable_res


def check_files(path, answer):
    path = Path(path)
    if not path.is_dir():
        return False
    files = [x.name for x in path.iterdir()]
    return set(files) == set(answer)


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_downloader_cards(mocker, cleanup):
    downloader = src.downloader.Downloader(Path("test/temp"), src.classes.Card)

    mocker.patch(
        "src.html_parser.ListParser.get_num_pages",
        return_value=test.mocks.mock_num_pages,
    )
    mocker.patch(
        "src.html_parser.ListParser.get_page",
        test.mocks.mock_page,
    )
    mocker.patch(
        "src.html_parser.CardParser.get_item",
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
    downloader = src.downloader.Downloader(Path("test/temp"), src.classes.Still)

    mocker.patch(
        "src.html_parser.ListParser.get_num_pages",
        return_value=test.mocks.mock_num_pages,
    )
    mocker.patch(
        "src.html_parser.ListParser.get_page",
        test.mocks.mock_page,
    )
    mocker.patch(
        "src.html_parser.StillParser.get_item",
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
