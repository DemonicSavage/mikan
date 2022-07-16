from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import utils

if TYPE_CHECKING:
    from classes import Item


class Organizer:
    def __init__(self, path: Path, img_type: type[Item]):
        self.path: Path = utils.init_path(path)
        self.organizer: CardOrganizer | StillOrganizer = img_type.get_organizer(
            self.path)
        self.results_dir: str = img_type.get_folder()

    def get_filenames(self, suffix_list: list[str]) -> list[Path]:
        _dir: list[Path] = [x for x in (self.path/self.results_dir).iterdir()
                            if x.is_file() and x.suffix in suffix_list]
        return _dir

    def remove_partially_downloaded(self) -> None:
        files: list[Path] = self.get_filenames([".part"])
        for file in files:
            file.unlink()

    def organize(self) -> None:
        self.organizer.remove_duplicates(self.get_filenames([".png", ".jpeg"]))
        self.organizer.create_symlinks(self.get_filenames([".png", ".jpeg"]))

        self.remove_partially_downloaded()


class CardOrganizer:

    def __init__(self, path: Path):
        self.path: Path = path

    def remove_duplicates(self, paths: list[Path]) -> None:
        prefixes: list[str] = [str(prefix).split(
            ".", maxsplit=1)[0] for prefix in paths]

        for path in prefixes:
            if prefixes.count(path) > 1:
                jpg: Path = Path(f"{path}.jpeg")
                try:
                    jpg.unlink()

                    jpg_name: str = jpg.name
                    split_jpg: list[str] = jpg_name.split("_")

                    (Path(self.path) /
                     split_jpg[1] / split_jpg[2] / jpg_name).unlink()

                except FileNotFoundError:
                    pass

    def create_symlink(self, path: Path) -> None:
        file_name: str = path.name
        name: list[str] = file_name.split("_")
        new_path: Path = Path(self.path) / name[1] / name[2]
        new_card: Path = new_path / file_name

        utils.init_path(new_path)
        try:
            new_card.symlink_to(path)

            print(f"Symlinked to {name[1]}/{name[2]}/{file_name}.")
        except FileExistsError:
            pass

    def create_symlinks(self, paths: list[Path]) -> None:
        for card in paths:
            self.create_symlink(card)


class StillOrganizer:

    def __init__(self, path: Path):
        self.path: Path = path

    def remove_duplicates(self, paths: list[Path]) -> None:
        prefixes: list[str] = [str(prefix).split(
            ".", maxsplit=1)[0] for prefix in paths]

        for path in prefixes:
            if prefixes.count(path) > 1:
                jpg: Path = Path(f"{path}.jpeg")
                try:
                    jpg.unlink()
                except FileNotFoundError:
                    pass

    def create_symlinks(self, paths: list[Path]) -> None:
        pass
