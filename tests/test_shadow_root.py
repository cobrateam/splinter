import pytest

from .fake_webapp import EXAMPLE_APP
from splinter.driver.webdriver import ShadowRootElement


supported_browsers = ["chrome", "chrome_fullscreen"]


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_shadow_root(browser_name, get_new_browser):
    """The shadow_root property will return a ShadowRootElement."""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    element = browser.find_by_id("has_shadow_root")
    shadow_root = element.shadow_root
    assert isinstance(shadow_root, ShadowRootElement)


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_shadow_root_element_find_by_css(browser_name, get_new_browser):
    """ShadowRootElement implements ElementAPI.find_by_css."""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    element = browser.find_by_id("has_shadow_root")
    shadow_root = element.shadow_root

    inner_element = shadow_root.find_by_css("#text_in_shadow_root")
    assert "Inside a shadow root" == inner_element.value


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_shadow_root_element_find_by_name(browser_name, get_new_browser):
    """ShadowRootElement implements ElementAPI.find_by_value."""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    element = browser.find_by_id("has_shadow_root")
    shadow_root = element.shadow_root

    inner_element = shadow_root.find_by_name("text_in_shadow_root_name")
    assert "Inside a shadow root" == inner_element.value
