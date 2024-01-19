import json
from pathlib import Path
import pytest
from mikan.json_utils import dump_to_file, load_cards


@pytest.fixture
def temp_directory(tmp_path):
    return tmp_path


def test_dump_to_file(temp_directory):
    cards = {"Mock": {}}
    expected_file_path = temp_directory / "items.json"

    dump_to_file(cards, temp_directory)

    assert expected_file_path.exists()
    with open(expected_file_path, "r", encoding="utf-8") as file:
        assert json.load(file) == cards


def test_load_cards(temp_directory):
    cards = {"Mock": {}}
    file_path = temp_directory / "items.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(cards, file)

    loaded_cards = load_cards(temp_directory)

    assert loaded_cards == cards


def test_load_cards_io_error(temp_directory, mocker):
    cards = {"Mock": {}}
    file_path = temp_directory / "items.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(cards, file)

    mocker.patch("builtins.open", side_effect=IOError("Error"))
    loaded_cards = load_cards(temp_directory)
    assert loaded_cards == {}


def test_dump_to_file_io_error(temp_directory, mocker):
    cards = {"Mock": {}}

    mocker.patch("builtins.open", side_effect=IOError("Error"))

    dump_to_file(cards, temp_directory)

    assert not (temp_directory / "items.json").exists()
