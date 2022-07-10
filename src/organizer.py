from pathlib import Path

import utils
import consts


class Organizer:
    def __init__(self, path, img_type):
        self.path = utils.init_path(path)
        self.organizer = img_type.get_organizer(self.path)
        self.results_dir = img_type.get_folder()

    def get_filenames(self, suffix_list):
        dir = [x for x in (self.path/self.results_dir).iterdir()
               if x.is_file() and x.suffix in suffix_list]
        return list(dir)

    def remove_partially_downloaded(self):
        files = self.get_filenames([".part"])
        for file in files:
            file.unlink()

    def organize(self):
        self.organizer.remove_duplicates(self.get_filenames([".png", ".jpeg"]))
        self.organizer.create_symlinks(self.get_filenames([".png", ".jpeg"]))

        self.remove_partially_downloaded()


class CardOrganizer:

    def __init__(self, path):
        self.path = path

    def remove_duplicates(self, paths):
        prefixes = [str(prefix).split(".")[0] for prefix in paths]

        for path in prefixes:
            if prefixes.count(path) > 1:
                jpg = Path(f"{path}.jpeg")
                try:
                    jpg.unlink()

                    jpg = jpg.name
                    split_jpg = jpg.split("_")

                    (Path(self.path) /
                     split_jpg[1] / split_jpg[2] / jpg).unlink()

                except FileNotFoundError:
                    pass

    def create_symlink(self, path):
        file_name = path.name
        name = file_name.split("_")
        new_path = Path(self.path) / name[1] / name[2]
        new_card = new_path / file_name

        utils.init_path(new_path)
        try:
            new_card.symlink_to(path)

            print(f"Symlinked to {name[1]}/{name[2]}/{file_name}.")
        except FileExistsError:
            pass

    def create_symlinks(self, paths):
        for card in paths:
            self.create_symlink(card)


class StillOrganizer:

    def __init__(self, path):
        self.path = path

    def remove_duplicates(self, paths):
        prefixes = [str(prefix).split(".")[0] for prefix in paths]

        for path in prefixes:
            if prefixes.count(path) > 1:
                jpg = Path(f"{path}.jpeg")
                try:
                    jpg.unlink()
                except FileNotFoundError:
                    pass

    def create_symlinks(self, paths):
        pass
