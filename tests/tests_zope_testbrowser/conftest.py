import pytest


@pytest.fixture()
def browser_kwargs():
    return {"wait_time": 0.1}
