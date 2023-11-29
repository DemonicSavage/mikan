import json
from mikan.plugins.sifasstills import SIFASStills
import test.mocks
from pathlib import Path

import aiohttp
import pytest

import mikan.downloader


def check_files(path, answer):
    path = Path(path)
    if not path.is_dir():
        return False
    files = [x.name for x in path.iterdir()]
    return set(files) == set(answer)


class MockSession:
    def __init__(self, item):
        self.item = item

    async def get(self, _):
        return self.item


@pytest.mark.usefixtures("_cleanup")
@pytest.mark.asyncio()
async def test_downloader_cards(mocker):
    downloader = mikan.downloader.Downloader(
        Path("test/temp"), Path("test/temp"), "SIFASStills", MockSession(test.mocks.mock_file)
    )

    mocker.patch(
        "mikan.html_parser.Parser.get_items",
        test.mocks.mock_get_items,
    )
    downloader.objs = test.mocks.mock_objs
    await downloader.update()
    await downloader.get()

    with Path("test/temp/items.json").open() as file:
        assert json.loads(file.read())["SIFAS_Stills"] == json.loads(test.mocks.cards_json)["SIFAS_Stills"]
    assert check_files(f"test/temp/SIFAS_Stills", test.mocks.still_files)


@pytest.mark.usefixtures("_cleanup")
@pytest.mark.asyncio()
async def test_downloader_fail(mocker):
    downloader = mikan.downloader.Downloader(
        Path("test/temp"), Path("test/temp"), "SIFASStills", MockSession(test.mocks.mock_file)
    )

    mocker.patch(
        "mikan.html_parser.Parser.get_items",
        test.mocks.mock_get_items,
    )
    mocker.patch("test.test_downloader.MockSession.get", side_effect=aiohttp.ClientError("Err"))

    downloader.objs = test.mocks.mock_objs
    await downloader.update()
    await downloader.get()

    assert not Path("test/temp/SIFAS_Stills").exists()


@pytest.mark.usefixtures("_cleanup")
@pytest.mark.asyncio()
async def test_downloader_card_load():
    directory = Path("test/temp")
    directory.mkdir(parents=True)
    with open(directory / "items.json", "w") as file:
        file.write(test.mocks.pre_json)
    downloader = mikan.downloader.Downloader(directory, directory, "SIFASStills", MockSession(test.mocks.mock_file))
    assert set(downloader.objs.keys()) == set(["SIFAS_Stills"])
