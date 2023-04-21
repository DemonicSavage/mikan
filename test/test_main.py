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

import pytest
import builtins

from mikan.main import Downloader, UnrecognizedArgumentException, run


@pytest.mark.asyncio
async def test_main(mocker):
    update = mocker.patch.object(Downloader, "update")
    get = mocker.patch.object(Downloader, "get")
    mocker.patch.object(builtins, "input", lambda _: "TestDir")
    mocker.patch("mikan.main.sys.argv", [])
    await run()
    update.assert_called()
    get.assert_called()


@pytest.mark.asyncio
async def test_main_stills(mocker):
    update = mocker.patch.object(Downloader, "update")
    get = mocker.patch.object(Downloader, "get")
    mocker.patch.object(builtins, "input", lambda _: "TestDir")
    mocker.patch("mikan.main.sys.argv", ["ex", "--stills"])
    await run()
    update.assert_called()
    get.assert_called()


@pytest.mark.asyncio
async def test_main_sif_cards(mocker):
    update = mocker.patch.object(Downloader, "update")
    get = mocker.patch.object(Downloader, "get")
    mocker.patch.object(builtins, "input", lambda _: "TestDir")
    mocker.patch("mikan.main.sys.argv", ["ex", "--sif"])
    await run()
    update.assert_called()
    get.assert_called()


@pytest.mark.asyncio
async def test_main_fail(mocker):
    mocker.patch.object(Downloader, "update")
    mocker.patch.object(Downloader, "get")
    mocker.patch.object(builtins, "input", lambda _: "TestDir")
    mocker.patch("mikan.main.sys.argv", ["ex", "--stlls"])
    with pytest.raises(UnrecognizedArgumentException) as ex:
        await run()
    assert ex.type == UnrecognizedArgumentException
