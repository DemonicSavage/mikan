#!/usr/bin/env python3

import argparse
import sys

from downloader import CardDownloader, StillDownloader
from organizer import CardOrganizer, StillOrganizer

import json_utils
import config


def main():
    argparser = argparse.ArgumentParser(
        prog="sifas_card_downloader", description="searches and downloads SIFAS cards")
    argparser.add_argument('--stills', action='store_true',
                           help='work with stills instead of cards (won\'t organize)')

    args = argparser.parse_args(args=None if sys.argv[1:] else ['--help'])
    card_searcher(config.CARDS_DIR, args)


def card_searcher(path, args):
    downloader = CardDownloader(
        path) if not args.stills else StillDownloader(path)
    organizer = CardOrganizer(
        path) if not args.stills else StillOrganizer(path)
    json_utils.load_cards(downloader.path, downloader.objs, still=args.stills)

    downloader.update()
    downloader.download()
    organizer.organize()


if __name__ == '__main__':
    main()
