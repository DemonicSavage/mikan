import pytest
import aiohttp

import src.classes
import src.html_parser
from test.mocks import MockResponse, awaitable_res

list_payload = MockResponse(
    """
    <div class='top-item'>
        <a href='/123/'></a>
    </div>
    """,
    200,
)
num_pages_payload = MockResponse(
    """
    <div class='pagination'>
        <a href='=1'></a>
        <a href='=42'></a>
        <a href='last'></a>
    </div>
    """,
    200,
)
card_payload = MockResponse(
    """
    <div class='top-item'>
        <a href='Normal'></a>
        <a href='Idolized'></a>
    </div>
    <table>
        <tbody>
            <tr data-field="idol">
                <td>null</td>
                <td><span>Name      Open idol</td>
            </tr>
            <tr data-field="rarity">
                <td>null</td>
                <td>Rarity</td>
            </tr>
            <tr data-field="attribute">
                <td>null</td>
                <td>Attribute</td>
            </tr>
            <tr data-field="i_unit">
                <td>null</td>
                <td>Unit</td>
            </tr>
            <tr data-field="i_subunit">
                <td>null</td>
                <td>Subunit</td>
            </tr>
            <tr data-field="i_year">
                <td>null</td>
                <td>Year</td>
            </tr>
        </tbody>
    </table>
    """,
    200,
)
still_payload = MockResponse(
    """
    <div class='top-item'>
        <a href='URL'></a>
    </div>
    """,
    200,
)


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
        "src.html_parser.aiohttp.ClientSession.get",
        return_value=awaitable_res(list_payload),
    )
    async with Parser(src.html_parser.ListParser(src.classes.Card)) as parser:
        assert await parser.parser.get_page(1) == [123]


@pytest.mark.asyncio
async def test_num_pages_parser(mocker):
    mocker.patch(
        "src.html_parser.aiohttp.ClientSession.get",
        return_value=awaitable_res(num_pages_payload),
    )
    async with Parser(src.html_parser.ListParser(src.classes.Card)) as parser:
        assert await parser.parser.get_num_pages() == 42


@pytest.mark.asyncio
async def test_card_parser(mocker):
    mocker.patch(
        "src.html_parser.aiohttp.ClientSession.get",
        return_value=awaitable_res(card_payload),
    )
    async with Parser(src.html_parser.CardParser()) as parser:
        assert await parser.parser.get_item(98) == (
            98,
            src.classes.Card(
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
        "src.html_parser.aiohttp.ClientSession.get",
        return_value=awaitable_res(still_payload),
    )
    async with Parser(src.html_parser.StillParser()) as parser:
        assert await parser.parser.get_item(98) == (
            98,
            src.classes.Still(
                98,
                "URL",
            ),
        )
