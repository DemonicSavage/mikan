from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict, cast

if TYPE_CHECKING:
    from src.classes import Item


class Consts(TypedDict):
    RESULTS_DIR: str
    LIST_URL_TEMPLATE: str
    URL_TEMPLATE: str
    JSON_FILENAME: str


card: Consts = {
    "RESULTS_DIR": "All",
    "LIST_URL_TEMPLATE": "https://idol.st/ajax/allstars/cards/?page=",
    "URL_TEMPLATE": "https://idol.st/ajax/allstars/card/",
    "JSON_FILENAME": "cards.json",
}

still: Consts = {
    "RESULTS_DIR": "Stills",
    "LIST_URL_TEMPLATE": "https://idol.st/ajax/allstars/stills/?page=",
    "URL_TEMPLATE": "https://idol.st/ajax/allstars/still/",
    "JSON_FILENAME": "stills.json",
}

item = {
    "Card": card,
    "Still": still,
}


def get_const(img_type: type[Item] | str, key: str) -> str:
    if isinstance(img_type, str):
        tp = item[img_type]
    else:
        tp = item[img_type.__name__]
    return cast(str, tp[key])
