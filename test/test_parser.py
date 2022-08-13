import test.mocks
from test.utils import awaitable_res

import aiohttp
import pytest

import sifas_card_downloader.classes
import sifas_card_downloader.html_parser


class Parser:
    def __init__(self, parser):
        self.parser = parser

    async def __aenter__(self):
        self.parser.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, a, b, c):
        await self.parser.session.close()


@pytest.mark.asyncio
async def test_list_parser(mocker):
    mocker.patch(
        "sifas_card_downloader.html_parser.aiohttp.ClientSession.get",
        return_value=awaitable_res(test.mocks.mock_list_response),
    )
    async with Parser(
        sifas_card_downloader.html_parser.ListParser(sifas_card_downloader.classes.Card)
    ) as parser:
        assert await parser.parser.get_page(1) == [123]


@pytest.mark.asyncio
async def test_num_pages_parser(mocker):
    mocker.patch(
        "sifas_card_downloader.html_parser.aiohttp.ClientSession.get",
        return_value=awaitable_res(test.mocks.mock_num_pages_response),
    )
    async with Parser(
        sifas_card_downloader.html_parser.ListParser(sifas_card_downloader.classes.Card)
    ) as parser:
        assert await parser.parser.get_num_pages() == 42


@pytest.mark.asyncio
async def test_card_parser(mocker):
    mocker.patch(
        "sifas_card_downloader.html_parser.aiohttp.ClientSession.get",
        return_value=awaitable_res(test.mocks.mock_card_response),
    )
    async with Parser(sifas_card_downloader.html_parser.CardParser()) as parser:
        assert await parser.parser.get_item(98) == (
            98,
            sifas_card_downloader.classes.Card(
                98,
                "Name",
                "Rarity",
                "Attribute",
                "Unit",
                "Subunit",
                "Year",
                "Normal",
                "Idolized",
            ),
        )


@pytest.mark.asyncio
async def test_still_parser(mocker):
    mocker.patch(
        "sifas_card_downloader.html_parser.aiohttp.ClientSession.get",
        return_value=awaitable_res(test.mocks.mock_still_response),
    )
    async with Parser(sifas_card_downloader.html_parser.StillParser()) as parser:
        assert await parser.parser.get_item(98) == (
            98,
            sifas_card_downloader.classes.Still(
                98,
                "URL",
            ),
        )


@pytest.mark.asyncio
async def test_list_parser_fail(mocker):
    mocker.patch(
        "sifas_card_downloader.html_parser.aiohttp.ClientSession.get",
        return_value=awaitable_res(test.mocks.mock_list_response_error),
    )
    async with Parser(
        sifas_card_downloader.html_parser.ListParser(sifas_card_downloader.classes.Card)
    ) as parser:
        with pytest.raises(
            sifas_card_downloader.html_parser.ListParsingException
        ) as ex:
            await parser.parser.get_page(1)
        assert ex.type == sifas_card_downloader.html_parser.ListParsingException


@pytest.mark.asyncio
async def test_num_pages_parser_fail(mocker):
    mocker.patch(
        "sifas_card_downloader.html_parser.aiohttp.ClientSession.get",
        return_value=awaitable_res(test.mocks.mock_num_pages_response_error),
    )
    async with Parser(
        sifas_card_downloader.html_parser.ListParser(sifas_card_downloader.classes.Card)
    ) as parser:
        with pytest.raises(
            sifas_card_downloader.html_parser.ListParsingException
        ) as ex:
            await parser.parser.get_num_pages()
        assert ex.type == sifas_card_downloader.html_parser.ListParsingException


@pytest.mark.asyncio
async def test_card_parser_fail(mocker):
    mocker.patch(
        "sifas_card_downloader.html_parser.aiohttp.ClientSession.get",
        return_value=awaitable_res(test.mocks.mock_card_response_error),
    )
    async with Parser(sifas_card_downloader.html_parser.CardParser()) as parser:
        with pytest.raises(
            sifas_card_downloader.html_parser.ItemParsingException
        ) as ex:
            await parser.parser.get_item(98)
    assert ex.type == sifas_card_downloader.html_parser.ItemParsingException


@pytest.mark.asyncio
async def test_card_parser_data_fail(mocker):
    mocker.patch(
        "sifas_card_downloader.html_parser.aiohttp.ClientSession.get",
        return_value=awaitable_res(test.mocks.mock_card_response_data_error),
    )
    async with Parser(sifas_card_downloader.html_parser.CardParser()) as parser:
        with pytest.raises(
            sifas_card_downloader.html_parser.ItemParsingException
        ) as ex:
            await parser.parser.get_item(98)
    assert ex.type == sifas_card_downloader.html_parser.ItemParsingException


@pytest.mark.asyncio
async def test_still_parser_fail(mocker):
    mocker.patch(
        "sifas_card_downloader.html_parser.aiohttp.ClientSession.get",
        return_value=awaitable_res(test.mocks.mock_still_response_error),
    )
    async with Parser(sifas_card_downloader.html_parser.StillParser()) as parser:
        with pytest.raises(
            sifas_card_downloader.html_parser.ItemParsingException
        ) as ex:
            await parser.parser.get_item(98)
    assert ex.type == sifas_card_downloader.html_parser.ItemParsingException


@pytest.mark.asyncio
async def test_parse_http_fail(mocker):
    parser = sifas_card_downloader.html_parser.CardParser()
    with pytest.raises(sifas_card_downloader.html_parser.NoHTTPSessionException) as ex:
        await parser.get_item(98)
    assert ex.type == sifas_card_downloader.html_parser.NoHTTPSessionException


@pytest.mark.asyncio
async def test_unimplemented(mocker):
    assert (
        sifas_card_downloader.html_parser.ListParser(
            sifas_card_downloader.classes.Card
        ).create_item(98)
        is None
    )
    assert sifas_card_downloader.html_parser.Parser().create_item(98) is None
    assert sifas_card_downloader.html_parser.Parser().get_url(98) is None
