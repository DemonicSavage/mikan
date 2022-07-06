from pathlib import Path
import os

import utils

import consts


class Organizer:
    def __init__(self, path):
        self.path = utils.init_path(path)

    def get_filenames(self, suffix_list):
        dir = [x for x in self.path.joinpath(
            self.results_dir).iterdir() if x.is_file() and x.suffix in suffix_list]
        return list(dir)

    def remove_partially_downloaded(self):
        files = self.get_filenames([".part"])
        for file in files:
            os.remove(file)


class CardOrganizer(Organizer):
    def __init__(self, path):
        super().__init__(path)
        self.data = []
        self.list = []

        self.results_dir = consts.CARD_RESULTS_DIR

    def remove_duplicates(self):
        paths = self.get_filenames([".jpg", ".png"])
        prefixes = [str(prefix).split(".")[0] for prefix in paths]

        for path in prefixes:
            if prefixes.count(path) > 1:
                jpg = Path(f"{path}.jpg")
                try:
                    os.remove(jpg)

                    jpg = jpg.name
                    split_jpg = jpg.split("_")

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
        self.remove_duplicates()

        cards = self.get_filenames([".jpg", ".png"])
        for card in cards:
            self.create_symlink(card)

        self.remove_partially_downloaded()


class StillOrganizer(Organizer):
    def __init__(self, path):
        super().__init__(path)
        self.results_dir = consts.STILL_RESULTS_DIR

    def remove_duplicates(self):
        paths = self.get_filenames([".jpg", ".png"])
        prefixes = [str(prefix).split(".")[0] for prefix in paths]

        for path in prefixes:
            if prefixes.count(path) > 1:
                jpg = Path(f"{path}.jpg")
                try:
                    os.remove(jpg)
                except FileNotFoundError:
                    pass

    def organize(self):
        self.remove_duplicates()
        self.remove_partially_downloaded()
