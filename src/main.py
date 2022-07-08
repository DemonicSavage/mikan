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
    argparser.add_argument('--all', action='store_true',
                           help='update, download, and organize cards')
    argparser.add_argument('--update', action='store_true',
                           help="update the json file containing card data to reflect the current available cards in idol.st")
    argparser.add_argument(
        '--download', action='store_true', help="download the cards")
    argparser.add_argument('--organize', action='store_true',
                           help="organize downloaded cards in a directory per unit, then a subdirectory per idol")
    argparser.add_argument('--stills', action='store_true',
                           help='work with stills instead of cards (won\'t organize)')

    args = argparser.parse_args(args=None if sys.argv[1:] else ['--help'])
    card_searcher(config.CARDS_DIR, args)


def card_searcher(path, args):
    downloader = CardDownloader(
        path) if not args.stills else StillDownloader(path)
    json_utils.load_cards(downloader.path, downloader.objs, still=args.stills)
    if args.update or args.all:
        downloader.update()
    if args.download or args.all:
        downloader.download()
    if args.organize or args.all:
        organizer = CardOrganizer(
            path) if not args.stills else StillOrganizer(path)
        organizer.organize()


if __name__ == '__main__':
    main()
