from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypedDict, cast

import html_parser
import organizer

if TYPE_CHECKING:
    from classes import Item


class Consts(TypedDict):
    RESULTS_DIR: str
    LIST_URL_TEMPLATE: str
    URL_TEMPLATE: str
    JSON_FILENAME: str
    PARSER: type[html_parser.CardParser | html_parser.StillParser]
    ORGANIZER: type[organizer.CardOrganizer | organizer.StillOrganizer]


card: Consts = {
    "RESULTS_DIR": "All",
    "LIST_URL_TEMPLATE": "https://idol.st/ajax/allstars/cards/?page=",
    "URL_TEMPLATE": "https://idol.st/ajax/allstars/card/",
    "JSON_FILENAME": "cards.json",
    "PARSER": html_parser.CardParser,
    "ORGANIZER": organizer.CardOrganizer,
}

still: Consts = {
    "RESULTS_DIR": "Stills",
    "LIST_URL_TEMPLATE": "https://idol.st/ajax/allstars/stills/?page=",
    "URL_TEMPLATE": "https://idol.st/ajax/allstars/still/",
    "JSON_FILENAME": "stills.json",
    "PARSER": html_parser.StillParser,
    "ORGANIZER": organizer.StillOrganizer,
}

item = {
    "Card": card,
    "Still": still,
}


def get_const(img_type: type[Item] | str, key: str) -> Any:
    if isinstance(img_type, str):
        tp = item[img_type]
    else:
        tp = item[img_type.__name__]
    return cast(Any, tp[key])
