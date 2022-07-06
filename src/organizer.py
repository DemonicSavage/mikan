from pathlib import Path
import os

import utils

import consts


class CardOrganizer:
    def __init__(self, path):
        self.path = utils.init_path(path)
        self.data = []
        self.list = []

    def get_filenames(self):
        dir = [x for x in self.path.joinpath(
            consts.CARD_RESULTS_DIR).iterdir() if x.is_file() and x.suffix in [".jpg", ".png"]]
        return list(dir)

    def remove_duplicates(self, paths):
        prefixes = [str(prefix).split(".")[0] for prefix in paths]

        for path in prefixes:
            if prefixes.count(path) > 1:
                jpg = Path(f"{path}.jpg")
                try:
                    os.remove(jpg)

                    jpg = jpg.name
                    split_jpg = self.split_filename(jpg)

                    os.unlink(Path.joinpath(
                        self.path, split_jpg[1], split_jpg[2], jpg))

                except FileNotFoundError:
                    pass

    def create_symlink(self, path):
        file_name = path.name
        name = file_name.split("_")
        new_path = Path.joinpath(self.path, name[1], name[2])
        new_card = new_path.joinpath(file_name)

        utils.init_path(new_path)
        try:
            new_card.symlink_to(path)

            print(f"Symlinked to {name[1]}/{name[2]}/{file_name}.")
        except FileExistsError:
            pass

    def organize(self):
        cards = self.get_filenames()
        self.remove_duplicates(cards)

        cards = self.get_filenames()
        for card in cards:
            self.create_symlink(card)


class StillOrganizer:
    def __init__(self, path):
        self.path = utils.init_path(path)

    def get_filenames(self):
        dir = [x for x in self.path.joinpath(
            consts.STILL_RESULTS_DIR).iterdir() if x.is_file() and x.suffix in [".jpg", ".png"]]
        return list(dir)

    def organize(self):
        paths = self.get_filenames()
        prefixes = [str(prefix).split(".")[0] for prefix in paths]

        for path in prefixes:
            if prefixes.count(path) > 1:
                jpg = Path(f"{path}.jpg")
                try:
                    os.remove(jpg)
                except FileNotFoundError:
                    pass
