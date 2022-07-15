import re

from dataclasses import dataclass
from pathlib import Path

import consts
import parser
import organizer
from typing import TypeAlias, Optional


@dataclass
class Idol:
    first_name: str
    last_name: str
    alt_spelling: Optional[str] = None


@dataclass
class Group:
    name: str
    idols: list[Idol]


@dataclass
class Card:
    key: int
    idol: str
    rarity: str
    attribute: str
    unit: str
    subunit: str
    year: str
    normal_url: str
    idolized_url: str

    def is_double_sized(self) -> bool:
        p: re.Pattern = re.compile(r"/2x/")
        return p.search(self.normal_url) != None

    def get_urls(self) -> list[str]:
        return [self.normal_url, self.idolized_url]

    def set_url(self, i: int, url: str) -> None:
        if i == 0:
            self.normal_url = url
        else:
            self.idolized_url = url

    def needs_update(self) -> bool:
        return not self.is_double_sized() and self.rarity != "Rare"

    def get_paths(self, path: Path) -> list[Path]:
        file_name: str = f"{self.key}_{self.unit}_{self.idol}"
        base_path: Path = Path(path) / consts.CARD_RESULTS_DIR

        normal_path: str = f"{file_name}_Normal{Path(self.normal_url).suffix}"
        idolized_path: str = normal_path.replace("Normal", "Idolized")

        return [base_path / normal_path, base_path / idolized_path]

    @staticmethod
    def get_folder() -> str:
        return consts.CARD_RESULTS_DIR

    @staticmethod
    def get_parser() -> parser.CardParser:
        return parser.CardParser()

    @staticmethod
    def get_list_parser() -> parser.ListParser:
        return parser.ListParser()

    @staticmethod
    def get_json_filename() -> str:
        return "cards.json"

    @staticmethod
    def get_organizer(path: Path) -> organizer.CardOrganizer:
        return organizer.CardOrganizer(path)


@dataclass
class Still:
    key: int
    url: str

    def is_double_sized(self) -> bool:
        p: re.Pattern = re.compile(r"/2x/")
        return p.search(self.url) != None

    def get_urls(self) -> list[str]:
        return [self.url]

    def set_url(self, i: int, url: str) -> None:
        self.url = url

    def needs_update(self) -> bool:
        return not self.is_double_sized()

    def get_paths(self, path: Path) -> list[Path]:
        file_name: str = f"{self.key}_Still"
        base_path: Path = Path(path) / consts.STILL_RESULTS_DIR

        return [base_path / f"{file_name}{Path(self.url).suffix}"]

    @staticmethod
    def get_folder() -> str:
        return consts.STILL_RESULTS_DIR

    @staticmethod
    def get_parser() -> parser.StillParser:
        return parser.StillParser()

    @staticmethod
    def get_list_parser() -> parser.ListParser:
        return parser.ListParser(still=True)

    @staticmethod
    def get_json_filename() -> str:
        return "stills.json"

    @staticmethod
    def get_organizer(path: Path) -> organizer.StillOrganizer:
        return organizer.StillOrganizer(path)


Item: TypeAlias = Card | Still
