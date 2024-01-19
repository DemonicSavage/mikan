import tempfile
from pathlib import Path
import pytest
from mikan.config import Config


@pytest.fixture
def config_file(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda x: "~/Idol_Cards")
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir)
        yield config_path


def test_config_initialization(config_file, monkeypatch):
    config = Config(config_file)
    assert config.data_dir == Path("~/Idol_Cards").expanduser().resolve()
    assert config.cookie == ""
    assert config.max_conn == 10


def test_config_initialization_with_existing_file(config_file):
    config_data = """
    [Paths]
    data_dir = /path/to/data
    [Other]
    cookie = secret_cookie
    max_connections = 20
    """
    with open(config_file / "config.cfg", "w") as file:
        file.write(config_data)

    config = Config(config_file)
    assert config.data_dir == Path("/path/to/data")
    assert config.cookie == "secret_cookie"
    assert config.max_conn == 20


def test_config_initialization_with_invalid_file(config_file, capsys):
    config_data = """
    [Paths]
    data_dir = /path/to/data
    [Other]
    cookie = invalid_cookie
    max_connections = invalid_value
    """
    with open(config_file / "config.cfg", "w") as file:
        file.write(config_data)

    Config(config_file)
    captured = capsys.readouterr()
    assert "Error occurred while reading the configuration file" in captured.out


def test_config_initialization_with_invalid_initial_config(config_file, capsys, mocker):
    mocker.patch("builtins.input", side_effect=ValueError())
    Config(config_file)
    captured = capsys.readouterr()
    assert "Error occurred while creating the initial configuration" in captured.out
