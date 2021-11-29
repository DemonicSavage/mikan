from dataclasses import dataclass
from typing import List

@dataclass
class Idol:
    first_name: str
    last_name: str
    alt_spelling: str = None

@dataclass
class Group:
    name: str
    idols: List[Idol]

@dataclass
class Card:
    num: int
    idol: str
    rarity: str
    attribute: str
    unit: str
    subunit: str
    year: str
    normal_url: str
    idolized_url: str