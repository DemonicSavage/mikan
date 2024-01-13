#!/usr/bin/env python3
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
from mikan.plugins.sifasstills import SIFASStills
import test.mocks
from pathlib import Path

import aiohttp
import pytest

import mikan.downloader
from mikan.plugins import registry


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


@pytest.fixture()
def downloader():
    registry["MockPlugin"] = test.mocks.MockPlugin()
    return mikan.downloader.Downloader(
        Path("test/temp"), Path("test/temp"), "MockPlugin", MockSession(test.mocks.mock_file)
    )


@pytest.mark.usefixtures("_cleanup")
@pytest.mark.asyncio()
async def test_downloader_cards(downloader):
    await downloader.update()
    await downloader.get()

    with Path("test/temp/items.json").open() as file:
        assert json.loads(file.read())["Mock"] == json.loads(test.mocks.cards_json)["Mock"]
    assert check_files(f"test/temp/Mock", test.mocks.card_files)


@pytest.mark.usefixtures("_cleanup")
@pytest.mark.asyncio()
async def test_downloader_fail(downloader, mocker):
    downloader.objs = json.loads(test.mocks.cards_json)

    mocker.patch("test.test_downloader.MockSession.get", side_effect=aiohttp.ClientError("Err"))

    with pytest.raises(aiohttp.ClientError):
        await downloader.update()

    await downloader.get()

    assert not Path("test/temp/Mock").exists()


@pytest.mark.usefixtures("_cleanup")
@pytest.mark.asyncio()
async def test_downloader_card_load():
    directory = Path("test/temp")
    directory.mkdir(parents=True)
    with open(directory / "items.json", "w") as file:
        file.write(test.mocks.cards_json)
    downloader = mikan.downloader.Downloader(directory, directory, "MockPlugin", MockSession(test.mocks.mock_file))
    assert set(downloader.objs.keys()) == set(["Mock"])
