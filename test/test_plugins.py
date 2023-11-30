import base64
import json
from sys import api_version
from test.mocks import mock_empty_response
from vcr import VCR

import aiohttp
import pytest

from mikan.html_parser import ParsingError
from mikan.main import discover_plugins
from mikan.plugins import registry

discover_plugins()

api_plugins = [plugin for _, plugin in registry.items() if plugin.is_api]
scraper_plugins = [plugin for _, plugin in registry.items() if not plugin.is_api]


class B64Serializer:
    def deserialize(cassette_string):
        decoded = base64.b64decode(bytes(cassette_string, "utf8"))
        return json.loads(decoded.decode("utf8"))

    def serialize(cassette_dict):
        encoded = base64.b64encode(bytes(json.dumps(cassette_dict), "utf8"))
        return encoded.decode("utf8")


@pytest.mark.parametrize("plugin", api_plugins + scraper_plugins)
@pytest.fixture()
def vcr_cassette_name(plugin):
    return f"cassette_{plugin.cli_arg}"


@pytest.fixture(scope="module")
def vcr(vcr):
    vcr.register_serializer("b64", B64Serializer)
    vcr.path_transformer = VCR.ensure_suffix(".b64")
    return vcr


async def get_test_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return resp


@pytest.mark.vcr(serializer="b64")
@pytest.mark.asyncio()
class TestPlugins:
    @pytest.mark.parametrize("plugin", scraper_plugins + api_plugins)
    async def test_plugin(self, vcr, plugin, vcr_cassette_name):
        first_page = await get_test_data(f"{plugin.list_url}{'' if plugin.is_api else '2'}")
        list_parser = plugin.ListParser()
        await list_parser.get_num_pages(first_page)
        if plugin.is_api:
            items = await list_parser.get_page(1)
        else:
            items = await list_parser.get_page(first_page)
        data = await get_test_data(f"{plugin.url}{items[0]}")
        urls = await plugin.ItemParser().create_item(data)
        assert len(urls) == 0 or all(
            "//" in url[:2] and (url.endswith(".png") or url.endswith(".jpg") or url.endswith(".jpeg")) for url in urls
        )

    @pytest.mark.parametrize("plugin", scraper_plugins)
    async def test_plugin_fail(self, mocker, plugin, vcr_cassette_name):
        if not plugin.is_api:
            with pytest.raises(ParsingError):
                await plugin.ListParser().get_num_pages(mock_empty_response)
            with pytest.raises(ParsingError):
                await plugin.ListParser().get_page(mock_empty_response)
            with pytest.raises(ParsingError):
                await plugin.ItemParser().create_item(mock_empty_response)
