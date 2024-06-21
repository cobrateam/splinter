import os

import pytest

from splinter.config import Config


xfail_if_safari = pytest.mark.xfail(
    os.getenv("SAFARI"),
    reason="Safari issues need to be investigated.",
)


@pytest.fixture(scope="session")
def browser_config():
    return Config(user_agent="iphone", headless=True)


@xfail_if_safari
def test_should_be_able_to_change_user_agent(browser, app_url):
    browser.visit(app_url + "useragent")

    assert "iphone" in browser.html
