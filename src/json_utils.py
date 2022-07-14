from pathlib import Path
import json

from classes import Card, Still


def to_json(cards):
    return json.dumps({key: value.__dict__ for (key, value) in cards.items()}, ensure_ascii=False, indent=4)


def dump_to_file(json_obj, path, img_type):
    card_path = Path(path) / img_type.get_json_filename()
    with open(card_path, "w", encoding='utf-8') as f:
        f.write(json_obj)


def read_json_file(path, cards, img_type):
    card_path = Path(path) / img_type.get_json_filename()
    with open(card_path, "r", encoding='utf-8') as f:
        data = f.read()
    card_data = json.loads(data)
    for key, card in card_data.items():
        cards[int(key)] = img_type(**card)


def load_cards(path, cards, img_type):
    card_path = Path(path) / img_type.get_json_filename()
    if card_path.is_file():
        read_json_file(path, cards, img_type)
