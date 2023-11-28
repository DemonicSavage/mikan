from typing import Any

from aiohttp import ClientResponse

registry: dict[str, type["Plugin"]] = {}


class Plugin:
    card_dir = ""
    url = ""
    list_url = ""
    cli_arg = ""
    desc = ""
    is_api = False

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        registry[cls.__name__] = cls

    class ListParser:
        async def get_page(self, _: Any) -> list[int]:
            return []

        async def get_num_pages(self, _: ClientResponse) -> int:
            return 98

    class ItemParser:
        async def create_item(self, _: ClientResponse) -> list[str]:
            return []
