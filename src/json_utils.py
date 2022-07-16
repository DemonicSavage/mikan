from pathlib import Path
import json
from typing import Mapping

from classes import Item


def to_json(cards: dict[int, Item]) -> str:
    return json.dumps({key: value.__dict__ for (key, value) in cards.items()},
                      ensure_ascii=False, indent=4)


def dump_to_file(json_obj: str, path: Path, img_type: type[Item]) -> None:
    card_path: Path = path / img_type.get_json_filename()
    with open(card_path, "w", encoding='utf-8') as f:
        f.write(json_obj)


def read_json_file(path: Path, cards: dict[int, Item], img_type: type[Item]) -> None:
    card_path: Path = path / img_type.get_json_filename()
    with open(card_path, "r", encoding='utf-8') as f:
        data = f.read()
        card_data: dict[str, Mapping] = json.loads(data)
    for key, card in card_data.items():
        cards[int(key)] = img_type(**card)


def load_cards(path: Path, cards: dict[int, Item], img_type: type[Item]) -> None:
    card_path: Path = path / img_type.get_json_filename()
    if card_path.is_file():
        read_json_file(path, cards, img_type)
