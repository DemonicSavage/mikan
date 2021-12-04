from pathlib import Path
import json

from classes import Card

def to_json(cards):
    return json.dumps({key: value.__dict__ for (key, value) in cards.items()}, ensure_ascii=False, indent=4)

def dump_to_file(json_obj, path):
    card_path = Path(path).joinpath("cards.json")
    with open(card_path, "w") as f:
        f.write(json_obj)

def read_json_file(path, cards):
    card_path = Path(path).joinpath("cards.json")
    with open(card_path, "r") as f:
        data = f.read()
    card_data = json.loads(data)
    for key, card in card_data.items():
        cards[int(key)] = Card(**card)

def load_cards(path, cards):
    card_path = Path(path).joinpath("cards.json")
    if card_path.is_file():
        read_json_file(path, cards)
    