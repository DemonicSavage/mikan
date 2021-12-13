#!/usr/bin/env python3

import argparse
import sys

from downloader import CardDownloader
from organizer import CardOrganizer

import json_utils
import config

def main():
    argparser = argparse.ArgumentParser(prog="sifas_card_downloader", description="searches and downloads SIFAS cards")
    argparser.add_argument('--organize', action='store_true', help="organize downloaded cards in a directory per unit, then a subdirectory per idol")
    argparser.add_argument('--update', action='store_true', help="update the json file containing card data to reflect the current available cards in idol.st")
    argparser.add_argument('--download', action='store_true', help="download the cards")
    # TODO: Do this:
    argparser.add_argument('--idol', action='store', help="search cards with provided idol name")
    argparser.add_argument('--rarity', action='store', help="search cards with provided card rarity")
    argparser.add_argument('--attribute', action='store', help="search cards with provided card attribute")
    argparser.add_argument('--unit', action='store', help="search cards with provided unit name")
    argparser.add_argument('--subunit', action='store', help="search cards with provided subunit name")
    argparser.add_argument('--year', action='store', help="search cards with provided school year")
    args = argparser.parse_args(args=None if sys.argv[1:] else ['--help'])
    card_searcher(config.CARDS_DIR, args)

def card_searcher(path, args):
    card_downloader = CardDownloader(path)
    json_utils.load_cards(card_downloader.path, card_downloader.cards)
    if args.update:
        card_downloader.update_cards()
    if args.download:
        card_downloader.download_cards()
    if args.organize:
        card_organizer = CardOrganizer(path)
        card_organizer.organize_cards()

if __name__=='__main__':
    main()