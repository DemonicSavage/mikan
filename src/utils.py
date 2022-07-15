from pathlib import Path


def init_path(path_name: Path) -> Path:
    path = path_name.expanduser()

    if not path.exists():
        path.mkdir(parents=True)

    return path
