from abc import ABC, abstractmethod
from pathlib import Path

from sifas_card_downloader.classes import Card, Still


class Organizer(ABC):
    def __init__(self, path: Path):
        self.path = path.expanduser()
        self.results_dir = ""

    def get_filenames(self, suffix_list: list[str]) -> list[Path]:
        _dir = [
            x
            for x in (self.path / self.results_dir).iterdir()
            if x.is_file() and x.suffix in suffix_list
        ]
        return _dir

    def remove_partially_downloaded(self) -> None:
        files = self.get_filenames([".part"])
        for file in files:
            file.unlink()

    def organize(self) -> None:
        self.remove_duplicates(self.get_filenames([".png", ".jpeg"]))
        self.create_symlinks(self.get_filenames([".png", ".jpeg"]))

        self.remove_partially_downloaded()

    @abstractmethod
    def remove_duplicates(self, paths: list[Path]) -> None:
        ...

    @abstractmethod
    def create_symlinks(self, paths: list[Path]) -> None:
        ...


class SIFCardOrganizer(Organizer):
    def __init__(self, path: Path):
        ...

    def organize(self) -> None:
        ...

    def remove_duplicates(self, paths: list[Path]) -> None:
        ...

    def create_symlinks(self, paths: list[Path]) -> None:
        ...


class CardOrganizer(Organizer):
    def __init__(self, path: Path):
        super().__init__(path)
        self.results_dir = Card.results_dir

    def remove_duplicates(self, paths: list[Path]) -> None:
        prefixes = [str(prefix).split(".", maxsplit=1)[0] for prefix in paths]

        for path in prefixes:
            if prefixes.count(path) > 1:
                jpg = Path(f"{path}.jpeg")
                try:
                    jpg.unlink()

                    jpg_name = jpg.name
                    split_jpg = jpg_name.split("_")

                    (self.path / split_jpg[1] / split_jpg[2] / jpg_name).unlink()

                except FileNotFoundError:
                    pass

    def create_symlink(self, path: Path) -> None:
        file_name = path.name
        name = file_name.split("_")
        new_path = self.path / name[1] / name[2]
        new_card = new_path / file_name

        new_path.mkdir(exist_ok=True, parents=True)
        try:
            new_card.symlink_to(path)

        except FileExistsError:
            pass

    def create_symlinks(self, paths: list[Path]) -> None:
        for card in paths:
            self.create_symlink(card)


class StillOrganizer(Organizer):
    def __init__(self, path: Path):
        super().__init__(path)
        self.results_dir = Still.results_dir

    def remove_duplicates(self, paths: list[Path]) -> None:
        prefixes = [str(prefix).split(".", maxsplit=1)[0] for prefix in paths]

        for path in prefixes:
            if prefixes.count(path) > 1:
                jpg = Path(f"{path}.jpeg")
                try:
                    jpg.unlink()
                except FileNotFoundError:
                    pass

    def create_symlinks(self, paths: list[Path]) -> None:
        pass
