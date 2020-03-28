import os

from .base import get_browser
from .fake_webapp import EXAMPLE_APP

import pytest


supported_browsers = ['chrome', 'firefox']


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_attach_file(request, browser_name):
    """Should provide a way to change file field value"""
    browser = get_browser(browser_name)
    request.addfinalizer(browser.quit)

    file_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "mockfile.txt"
    )

    browser.visit(EXAMPLE_APP)
    browser.attach_file("file", file_path)
    browser.find_by_name("upload").click()

    html = browser.html
    assert "text/plain" in html

    with open(file_path, "r") as f:
        assert str(f.read().encode("utf-8")) in html


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_should_support_with_statement(browser_name):
    with get_browser(browser_name):
        pass
