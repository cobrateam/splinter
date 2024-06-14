import os
import pathlib

import pytest

from tests.fake_webapp import EXAMPLE_APP

from splinter.config import Config


@pytest.fixture(scope="session")
def browser_config():
    extension_path = pathlib.Path(
        os.getcwd(),  # NOQA PTH109
        "tests",
        "dummy_extension",
        "borderify-1.0-an+fx.xpi",
    )

    return Config(extensions=[str(extension_path)], headless=True)


def test_firefox_create_instance_with_extension(request, browser):
    """Test: Load an extension via selenium.

    The dummy extension should add a red border to any web page.
    """
    request.addfinalizer(browser.quit)

    browser.visit(EXAMPLE_APP)

    elem = browser.find_by_css("body")
    elem.is_visible(wait_time=20)

    style = elem._element.get_attribute("style")
    assert "border: 5px solid red;" == style
