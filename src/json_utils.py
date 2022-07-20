import json
from pathlib import Path
from typing import Any

import consts
from classes import Item


def to_json(cards: dict[int, Item]) -> str:
    return json.dumps(
        {key: value.__dict__ for (key, value) in cards.items()},
        ensure_ascii=False,
        indent=4,
    )


def dump_to_file(json_obj: str, path: Path, img_type: type[Item]) -> None:
    card_path: Path = path / consts.get_const(img_type, "JSON_FILENAME")
    with open(card_path, "w", encoding="utf-8") as file:
        file.write(json_obj)


def read_json_file(path: Path, cards: dict[int, Item], img_type: type[Item]) -> None:
    card_path: Path = path / consts.get_const(img_type, "JSON_FILENAME")
    with open(card_path, "r", encoding="utf-8") as file:
        data = file.read()
    card_data: dict[str, Any] = json.loads(data)

    for key, card in card_data.items():
        cards[int(key)] = img_type(**card)


def load_cards(path: Path, cards: dict[int, Item], img_type: type[Item]) -> None:
    card_path: Path = path / consts.get_const(img_type, "JSON_FILENAME")
    if card_path.is_file():
        read_json_file(path, cards, img_type)
