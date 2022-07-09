#!/usr/bin/env python3

import sys

from downloader import CardDownloader, StillDownloader
from organizer import CardOrganizer, StillOrganizer

import json_utils
import config


class UnrecognizedArgumentException(Exception):
    pass


def main():
    work_with_stills = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "--stills":
            work_with_stills = True
        else:
            raise UnrecognizedArgumentException(
                "Only recognized argument is --stills.")

    card_searcher(config.CARDS_DIR, work_with_stills)


def card_searcher(path, stills):
    downloader = CardDownloader(
        path) if not stills else StillDownloader(path)
    organizer = CardOrganizer(
        path) if not stills else StillOrganizer(path)
    json_utils.load_cards(downloader.path, downloader.objs, still=stills)

    downloader.update()
    downloader.download()
    organizer.organize()


if __name__ == '__main__':
    main()
