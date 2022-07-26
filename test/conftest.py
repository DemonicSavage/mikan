import shutil

import pytest


@pytest.fixture(autouse=True)
def cleanup():
    yield
    shutil.rmtree("test/temp", ignore_errors=True)
