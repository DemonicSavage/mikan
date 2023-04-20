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

import json
from pathlib import Path

from mikan.classes import Item


def to_json(cards: dict[int, Item]) -> str:
    return json.dumps(
        {key: value.__dict__ for (key, value) in cards.items()},
        ensure_ascii=False,
        indent=4,
    )


def dump_to_file(json_obj: str, path: Path, img_type: type[Item]) -> None:
    card_path = path / img_type.json_filename
    card_path.parent.mkdir(exist_ok=True, parents=True)
    with open(card_path, "w", encoding="utf-8") as file:
        file.write(json_obj)


def read_json_file(path: Path, cards: dict[int, Item], img_type: type[Item]) -> None:
    card_path = path / img_type.json_filename
    with open(card_path, "r", encoding="utf-8") as file:
        data = file.read()
    card_data = json.loads(data)

    for key, card in card_data.items():
        cards[int(key)] = img_type(**card)


def load_cards(path: Path, cards: dict[int, Item], img_type: type[Item]) -> None:
    card_path = path / img_type.json_filename
    if card_path.is_file():
        read_json_file(path, cards, img_type)
