#!/usr/bin/env python3
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

from abc import ABC, abstractmethod, abstractproperty
from typing import Any

from aiohttp import ClientResponse

from mikan.plugins import registry


class DefaultPlugin(ABC):
    is_api = False

    @abstractproperty
    def card_dir(self) -> str:
        pass

    @abstractproperty
    def url(self) -> str:
        pass

    @abstractproperty
    def list_url(self) -> str:
        pass

    @abstractproperty
    def cli_arg(self) -> str:
        pass

    @abstractproperty
    def desc(self) -> str:
        pass

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        registry[cls.__name__] = cls

    @staticmethod
    def item_renamer_fn(url: str) -> str:
        return url.split("/")[-1]

    class ListParser(ABC):
        @abstractmethod
        async def get_page(self, _: Any) -> list[int]:
            pass

        @abstractmethod
        async def get_num_pages(self, _: ClientResponse) -> int:
            pass

    class ItemParser:
        @abstractmethod
        async def create_item(self, _: ClientResponse) -> list[str]:
            pass
