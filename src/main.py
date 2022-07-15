#!/usr/bin/env python3

import sys
import asyncio

from downloader import Downloader
from organizer import Organizer

from pathlib import Path
from classes import Card, Still, Item

import config


class UnrecognizedArgumentException(Exception):
    pass


async def main() -> None:
    img_type: type[Item] = Card
    if len(sys.argv) > 1:
        if sys.argv[1] == "--stills":
            img_type = Still
        else:
            raise UnrecognizedArgumentException(
                "Only recognized argument is --stills.")

    await card_searcher(Path(config.CARDS_DIR), img_type)


async def card_searcher(path: Path, img_type: type[Item]):
    organizer: Organizer = Organizer(path, img_type)

    async with Downloader(path, img_type) as downloader:
        await downloader.update()
        await downloader.download()

    organizer.organize()


if __name__ == '__main__':
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
