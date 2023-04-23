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


def to_json(cards: dict[str, dict[str, list[str]]]) -> str:
    return json.dumps(
        cards,
        ensure_ascii=False,
        indent=4,
    )


def dump_to_file(cards: dict[str, dict[str, list[str]]], path: Path) -> None:
    json_path = path / "items.json"
    json_path.parent.mkdir(exist_ok=True, parents=True)
    with open(json_path, "w", encoding="utf-8") as file:
        file.write(to_json(cards))


def load_cards(cards: dict[str, dict[str, list[str]]], path: Path) -> None:
    json_path = path / "items.json"
    if json_path.is_file():
        with open(json_path, "r", encoding="utf-8") as file:
            data = file.read()
            new_cards = json.loads(data)
            for key, value in new_cards.items():
                cards[key] = value
