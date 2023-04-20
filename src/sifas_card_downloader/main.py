#!/usr/bin/env python3
# Copyright (C) 2022-2023 DemonicSavage
# This file is part of SIFAS Card Downloader.

# SIFAS Card Downloader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.

# SIFAS Card Downloader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License


import asyncio
import sys
from pathlib import Path
from typing import Type

from sifas_card_downloader import config, organizer
from sifas_card_downloader.classes import Card, Item, SIFCard, Still
from sifas_card_downloader.downloader import Downloader


class UnrecognizedArgumentException(Exception):
    pass


async def run() -> None:
    img_type: Type[Card | Still | SIFCard] = Card
    if len(sys.argv) > 1:
        if sys.argv[1] == "--stills":
            img_type = Still
        elif sys.argv[1] == "--sif":
            img_type = SIFCard
        else:
            raise UnrecognizedArgumentException(
                "Only recognized arguments are --stills and --sif."
            )

    await card_searcher(config.CARDS_DIR, img_type)


async def card_searcher(path: Path, img_type: type[Item]) -> None:
    item_organizer = getattr(organizer, f"{img_type.__name__}Organizer")

    async with Downloader(path, img_type) as downloader:
        await downloader.update()
        await downloader.get()

    item_organizer(path).organize()


def main() -> None:  # pragma: no cover
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(run())


if __name__ == "__main__":  # pragma: no cover
    main()
