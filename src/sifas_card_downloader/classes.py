import re
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, TypeAlias


@dataclass
class Card:
    results_dir: ClassVar = "All"
    list_url_template: ClassVar = "https://idol.st/ajax/allstars/cards/?page="
    url_template: ClassVar = "https://idol.st/ajax/allstars/card/"
    json_filename: ClassVar = "cards.json"

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
        pattern = re.compile(r"/2x/")
        return pattern.search(self.normal_url) is not None

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
        file_name = f"{self.key}_{self.unit}_{self.idol}"
        base_path = path / self.results_dir

        normal_path = f"{file_name}_Normal{Path(self.normal_url).suffix}"
        idolized_path = normal_path.replace("Normal", "Idolized")

        return [base_path / normal_path, base_path / idolized_path]


@dataclass
class Still:
    results_dir: ClassVar = "Stills"
    list_url_template: ClassVar = "https://idol.st/ajax/allstars/stills/?page="
    url_template: ClassVar = "https://idol.st/ajax/allstars/still/"
    json_filename: ClassVar = "stills.json"

    key: int
    url: str

    def is_double_sized(self) -> bool:
        pattern = re.compile(r"/2x/")
        return pattern.search(self.url) is not None

    def get_urls(self) -> list[str]:
        return [self.url]

    def set_url(self, _: int, url: str) -> None:
        self.url = url

    def needs_update(self) -> bool:
        return not self.is_double_sized()

    def get_paths(self, path: Path) -> list[Path]:
        file_name = f"{self.key}_Still"
        base_path = path / self.results_dir

        return [base_path / f"{file_name}{Path(self.url).suffix}"]


Item: TypeAlias = Card | Still
