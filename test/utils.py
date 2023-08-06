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

import asyncio


class MockIterator:
    def __init__(self, text):
        self._text = text

    def __anext__(self):
        raise StopAsyncIteration

    def __aiter__(self):
        return MockIterator(self._text)


class MockContent:
    def __init__(self, text):
        self._text = text

    def iter_any(self):
        return MockIterator(self._text)


class MockResponse:
    def __init__(self, text, status):
        self._text = text
        self.status = status
        self.content = MockContent(self._text)

    async def text(self):
        return self._text

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


def awaitable_res(res):
    f = asyncio.Future()
    f.set_result(res)
    return f
