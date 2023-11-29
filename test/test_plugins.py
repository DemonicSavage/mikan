import aiohttp
import base64
import pytest
import json
from mikan.main import discover_plugins
from mikan.plugins import registry

discover_plugins()

plugins = [plugin for _, plugin in registry.items()]


class B64Serializer:
    def deserialize(cassette_string):
        decoded = base64.b64decode(bytes(cassette_string, "utf8"))
        return json.loads(decoded.decode("utf8"))

    def serialize(cassette_dict):
        encoded = base64.b64encode(bytes(json.dumps(cassette_dict), "utf8"))
        return encoded.decode("utf8")


@pytest.fixture(scope="module")
def vcr(vcr):
    vcr.register_serializer("b64", B64Serializer)
    return vcr


async def get_test_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return resp


@pytest.mark.parametrize("plugin", plugins)
@pytest.mark.vcr(serializer="b64")
@pytest.mark.asyncio()
async def test_plugin(vcr, plugin):
    first_page = await get_test_data(f"{plugin.list_url}{'' if plugin.is_api else '2'}")
    list_parser = plugin.ListParser()
    num_pages = await list_parser.get_num_pages(first_page)
    if plugin.is_api:
        items = await list_parser.get_page(1)
    else:
        items = await list_parser.get_page(first_page)
    data = await get_test_data(f"{plugin.url}{items[0]}")
    await plugin.ItemParser().create_item(data)
