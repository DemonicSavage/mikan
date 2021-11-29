from pathlib import Path
import utils

import config

class CardOrganizer:
    def __init__(self, path):
        self.path= utils.init_path(path)
        self.data = []
        self.list = []

    def split_filename(self, filename):
        return filename.split("_")

    def get_card_names(self):
        dir = [x for x in self.path.joinpath(config.CARD_RESULTS_DIR).iterdir() if x.is_file()]
        return list(dir)

    def create_symlink(self, path):
        file_name = path.name
        name = self.split_filename(file_name)
        new_path = Path.joinpath(self.path, name[1], name[2])
        new_card = new_path.joinpath(file_name)

        utils.init_path(new_path)
        try:
            new_card.symlink_to(path)
            
            print(f"Symlinked to {name[1]}/{name[2]}/{file_name}.")
        except FileExistsError:
            print(f"File already symlinked: {file_name}.")
    
    def organize_cards(self):
        cards = self.get_card_names()
        for card in cards:
            self.create_symlink(card)
