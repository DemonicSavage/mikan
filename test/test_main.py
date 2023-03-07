import pytest

from sifas_card_downloader.main import Downloader, UnrecognizedArgumentException, run
from sifas_card_downloader.organizer import (
    CardOrganizer,
    StillOrganizer,
    SIFCardOrganizer,
)


@pytest.mark.asyncio
async def test_main(mocker):
    update = mocker.patch.object(Downloader, "update")
    get = mocker.patch.object(Downloader, "get")
    organizer = mocker.patch.object(CardOrganizer, "organize")
    mocker.patch("sifas_card_downloader.main.sys.argv", [])
    await run()
    update.assert_called()
    get.assert_called()
    organizer.assert_called()


@pytest.mark.asyncio
async def test_main_stills(mocker):
    update = mocker.patch.object(Downloader, "update")
    get = mocker.patch.object(Downloader, "get")
    organizer = mocker.patch.object(StillOrganizer, "organize")
    mocker.patch("sifas_card_downloader.main.sys.argv", ["ex", "--stills"])
    await run()
    update.assert_called()
    get.assert_called()
    organizer.assert_called()


@pytest.mark.asyncio
async def test_main_sif_cards(mocker):
    update = mocker.patch.object(Downloader, "update")
    get = mocker.patch.object(Downloader, "get")
    organizer = mocker.patch.object(SIFCardOrganizer, "organize")
    mocker.patch("sifas_card_downloader.main.sys.argv", ["ex", "--sif"])
    await run()
    update.assert_called()
    get.assert_called()
    organizer.assert_called()


@pytest.mark.asyncio
async def test_main_fail(mocker):
    mocker.patch.object(Downloader, "update")
    mocker.patch.object(Downloader, "get")
    mocker.patch("sifas_card_downloader.main.sys.argv", ["ex", "--stlls"])
    with pytest.raises(UnrecognizedArgumentException) as ex:
        await run()
    assert ex.type == UnrecognizedArgumentException
