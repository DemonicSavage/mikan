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

import pytest

import sifas_card_downloader.organizer


def create_mock_card_files(path, items):
    path = Path(path)
    path.mkdir(parents=True)
    for item in items:
        (path / item).touch()


def create_file(path):
    Path(path).touch()


def check_created_cards(n):
    directory = Path(f"test/temp/Unit{n}/Name{n}")
    files = [
        directory / f"{n}_Unit{n}_Name{n}_Idolized.png",
        directory / f"{n}_Unit{n}_Name{n}_Normal.png",
    ]
    return directory.is_dir() and set(files) == set(directory.iterdir())


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_organizer_cards(cleanup):
    organizer = sifas_card_downloader.organizer.CardOrganizer(Path("test/temp"))

    create_mock_card_files("test/temp/All", test.mocks.card_files)
    create_file("test/temp/All/1_Unit1_Name1_Normal.jpeg")
    create_file("test/temp/All/file.part")

    organizer.organize()
    organizer.create_symlink(Path("1_Unit1_Name1_Normal.png"))

    assert all(check_created_cards(n) for n in range(1, 7))


@pytest.mark.usefixtures("cleanup")
def test_organizer_sif_cards(cleanup):
    organizer = sifas_card_downloader.organizer.SIFCardOrganizer(Path("test/temp"))

    create_mock_card_files("test/temp/SIF", test.mocks.card_files)
    create_file("test/temp/SIF/file.part")
    organizer.organize()

    assert not Path("test/temp/SIF/file.part").exists()


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_organizer_stills(cleanup):
    organizer = sifas_card_downloader.organizer.StillOrganizer(Path("test/temp"))

    create_mock_card_files("test/temp/Stills", test.mocks.still_files)
    create_file("test/temp/Stills/1_Still.jpeg")
    create_file("test/temp/Stills/file.part")

    organizer.organize()
    assert not Path("test/temp/Stills/1_Still.jpeg").exists()
    assert not Path("test/temp/Stills/file.part").exists()


@pytest.mark.asyncio
async def test_unimplemented(cleanup):
    with pytest.raises(TypeError) as ex:
        assert (
            sifas_card_downloader.organizer.Organizer(
                Path("test/temp")
            ).remove_duplicates([])
            is None
        )
        assert (
            sifas_card_downloader.organizer.Organizer(
                Path("test/temp")
            ).create_symlinks([])
            is None
        )
    assert ex.type == TypeError
