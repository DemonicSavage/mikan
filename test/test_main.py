import pytest

from src.main import run, UnrecognizedArgumentException, Downloader
from src.organizer import CardOrganizer, StillOrganizer


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_main(mocker):
    update = mocker.patch.object(Downloader, "update")
    get = mocker.patch.object(Downloader, "get")
    organizer = mocker.patch.object(CardOrganizer, "organize")
    mocker.patch("src.main.sys.argv", [])
    await run()
    update.assert_called()
    get.assert_called()
    organizer.assert_called()


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_main_stills(mocker):
    update = mocker.patch.object(Downloader, "update")
    get = mocker.patch.object(Downloader, "get")
    organizer = mocker.patch.object(StillOrganizer, "organize")
    mocker.patch("src.main.sys.argv", ["ex", "--stills"])
    await run()
    update.assert_called()
    get.assert_called()
    organizer.assert_called()


@pytest.mark.usefixtures("cleanup")
@pytest.mark.asyncio
async def test_main_fail(mocker):
    mocker.patch.object(Downloader, "update")
    mocker.patch.object(Downloader, "get")
    mocker.patch("src.main.sys.argv", ["ex", "--stlls"])
    with pytest.raises(UnrecognizedArgumentException) as ex:
        await run()
    assert ex.type == UnrecognizedArgumentException
