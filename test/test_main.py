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

import argparse
import builtins

import pytest
from mikan.classes import Card, SIF2Card, SIFCard, Still
from mikan.main import Downloader, parse_arguments, run


@pytest.mark.asyncio()
async def test_main(mocker, tmp_path):
    update = mocker.patch.object(Downloader, "update")
    get = mocker.patch.object(Downloader, "get")
    mocker.patch.object(builtins, "input", return_value="test_dir")
    await run(argparse.Namespace(type=SIF2Card), tmp_path)
    update.assert_called()
    get.assert_called()


def test_argparser():
    args = parse_arguments([])
    assert args.type == SIF2Card


@pytest.mark.asyncio()
async def test_main_default_dir(mocker, tmp_path):
    update = mocker.patch.object(Downloader, "update")
    get = mocker.patch.object(Downloader, "get")
    mocker.patch.object(builtins, "input", return_value="\n")
    await run(argparse.Namespace(type=SIF2Card), tmp_path)
    update.assert_called()
    get.assert_called()


@pytest.mark.asyncio()
async def test_main_stills(mocker, tmp_path):
    update = mocker.patch.object(Downloader, "update")
    get = mocker.patch.object(Downloader, "get")
    mocker.patch.object(builtins, "input", return_value="test_dir")
    await run(argparse.Namespace(type=Still), tmp_path)
    update.assert_called()
    get.assert_called()


@pytest.mark.asyncio()
async def test_main_sif_cards(mocker, tmp_path):
    update = mocker.patch.object(Downloader, "update")
    get = mocker.patch.object(Downloader, "get")
    mocker.patch.object(builtins, "input", return_value="test_dir")
    await run(argparse.Namespace(type=SIFCard), tmp_path)
    update.assert_called()
    get.assert_called()


@pytest.mark.asyncio()
async def test_main_sifas_cards(mocker, tmp_path):
    update = mocker.patch.object(Downloader, "update")
    get = mocker.patch.object(Downloader, "get")
    mocker.patch.object(builtins, "input", return_value="test_dir")
    await run(argparse.Namespace(type=Card), tmp_path)
    update.assert_called()
    get.assert_called()
