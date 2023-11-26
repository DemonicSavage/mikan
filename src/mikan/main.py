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

import argparse
import asyncio
import sys
from importlib.metadata import version
from pathlib import Path

import aiohttp
import platformdirs

from mikan import config
from mikan.classes import Card, CardType, SIF2Card, SIFCard, Still
from mikan.downloader import Downloader

MIKAN_PACKAGE = "mikan_card_downloader"
MIKAN_PATH = Path(platformdirs.user_config_dir("mikan", ensure_exists=True))


class InvalidPathError(Exception):
    pass


def parse_arguments(args: list[str]) -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Downloads cards from idol.st and schoolido.lu. By default "
        "(with no arguments passed), it downloads SIF 2 cards.",
    )
    arg_parser.set_defaults(type=SIF2Card)

    group = arg_parser.add_mutually_exclusive_group()

    arg_parser.add_argument(
        "-v", "--version", action="version", version=f"Mikan {version(MIKAN_PACKAGE)}\nPython {sys.version}"
    )
    group.add_argument("--sifas", action="store_const", help="download SIFAS cards", dest="type", const=Card)
    group.add_argument("--stills", action="store_const", help="download SIFAS stills", dest="type", const=Still)
    group.add_argument("--sif", action="store_const", help="download SIF cards", dest="type", const=SIFCard)

    return arg_parser.parse_args(args)


async def run(arguments: argparse.Namespace, path: Path = MIKAN_PATH) -> None:
    cfg = config.Config(path)

    data_dir = cfg.data_dir
    if data_dir.exists() and not data_dir.is_dir():  # pragma: no cover
        raise InvalidPathError("The specified directory is not valid (it's a regular file).")

    await card_searcher(data_dir, path, arguments.type, cfg)


async def card_searcher(data_path: Path, config_path: Path, img_type: CardType, cfg: config.Config) -> None:
    http_session = aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(limit=cfg.max_conn, limit_per_host=cfg.max_conn),
        timeout=aiohttp.ClientTimeout(total=None),
        cookies={"sessionid": cfg.cookie},
    )

    async with http_session as session:
        downloader = Downloader(data_path, config_path, img_type, session)
        await downloader.update()
        await downloader.get()


def main() -> None:  # pragma: no cover
    args = parse_arguments(sys.argv[1:])
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(run(args))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":  # pragma: no cover
    main()
