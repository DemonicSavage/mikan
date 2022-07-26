import pytest
import shutil


@pytest.fixture(autouse=True)
def cleanup():
    yield
    shutil.rmtree("test/temp", ignore_errors=True)
