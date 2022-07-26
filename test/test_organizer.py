import test.mocks
from pathlib import Path

import pytest

import src.organizer


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
    organizer = src.organizer.CardOrganizer(Path("test/temp"))

    create_mock_card_files("test/temp/All", test.mocks.card_files)
    create_file("test/temp/All/1_Unit1_Name1_Normal.jpeg")
    create_file("test/temp/All/file.part")

    organizer.organize()
    organizer.create_symlink(Path("1_Unit1_Name1_Normal.png"))

    assert all(check_created_cards(n) for n in range(1, 7))


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_organizer_stills(cleanup):
    organizer = src.organizer.StillOrganizer(Path("test/temp"))

    create_mock_card_files("test/temp/Stills", test.mocks.still_files)
    create_file("test/temp/Stills/1_Still.jpeg")
    create_file("test/temp/Stills/file.part")

    organizer.organize()
    assert not Path("test/temp/Stills/1_Still.jpeg").exists()
    assert not Path("test/temp/Stills/file.part").exists()


@pytest.mark.asyncio
async def test_unimplemented(cleanup):
    assert src.organizer.Organizer(Path("test/temp")).remove_duplicates([]) is None
    assert src.organizer.Organizer(Path("test/temp")).create_symlinks([]) is None
