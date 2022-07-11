#!/usr/bin/env python3

import sys
import asyncio

from downloader import Downloader
from organizer import Organizer

from classes import Card, Still

import json_utils
import config


class UnrecognizedArgumentException(Exception):
    pass


async def main():
    img_type = Card
    if len(sys.argv) > 1:
        if sys.argv[1] == "--stills":
            img_type = Still
        else:
            raise UnrecognizedArgumentException(
                "Only recognized argument is --stills.")

    await card_searcher(config.CARDS_DIR, img_type)


async def card_searcher(path, img_type):
    downloader = Downloader(path, img_type)
    organizer = Organizer(path, img_type)
    json_utils.load_cards(downloader.path, downloader.objs, img_type)

    await downloader.update()
    await downloader.download()
    organizer.organize()


if __name__ == '__main__':
    asyncio.run(main())
