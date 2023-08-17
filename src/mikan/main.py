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


import asyncio
import sys
from pathlib import Path

import platformdirs

from mikan import config
from mikan.classes import Card, CardType, SIF2Card, SIFCard, Still
from mikan.downloader import Downloader

MIKAN_PATH = Path(platformdirs.user_config_dir("mikan", ensure_exists=True))


class UnrecognizedArgumentException(Exception):
    pass


class InvalidPathException(Exception):
    pass


async def run(path: Path = MIKAN_PATH) -> None:
    img_type: CardType = SIF2Card
    if len(sys.argv) > 1:
        if sys.argv[1] == "--stills":
            img_type = Still
        elif sys.argv[1] == "--sif":
            img_type = SIFCard
        elif sys.argv[1] == "--sifas":
            img_type = Card
        else:
            raise UnrecognizedArgumentException("Only recognized arguments are --stills, --sif and --sifas.")

    cfg = config.Config(path)

    data_dir = cfg.data_dir
    if data_dir.exists() and not data_dir.is_dir():  # pragma: no cover
        raise InvalidPathException("The specified directory is not valid (is a regular file).")

    await card_searcher(data_dir, path, img_type, cfg)


async def card_searcher(data_path: Path, config_path: Path, img_type: CardType, cfg: config.Config) -> None:
    async with Downloader(data_path, config_path, img_type, cfg) as downloader:
        await downloader.update()
        await downloader.get()


def main() -> None:  # pragma: no cover
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(run())
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":  # pragma: no cover
    main()
