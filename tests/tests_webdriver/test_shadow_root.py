from tests.fake_webapp import EXAMPLE_APP
from splinter.driver.webdriver import ShadowRootElement


def test_shadow_root(browser):
    """The shadow_root property will return a ShadowRootElement."""
    browser.visit(EXAMPLE_APP)

    element = browser.find_by_id("has_shadow_root")
    shadow_root = element.shadow_root
    assert isinstance(shadow_root, ShadowRootElement)


def test_shadow_root_element_find_by_css(browser):
    """ShadowRootElement implements ElementAPI.find_by_css."""
    browser.visit(EXAMPLE_APP)

    element = browser.find_by_id("has_shadow_root")
    shadow_root = element.shadow_root

    inner_element = shadow_root.find_by_css("#text_in_shadow_root")
    assert "Inside a shadow root" == inner_element.value


def test_shadow_root_element_find_by_name(browser):
    """ShadowRootElement implements ElementAPI.find_by_value."""
    browser.visit(EXAMPLE_APP)

    element = browser.find_by_id("has_shadow_root")
    shadow_root = element.shadow_root

    inner_element = shadow_root.find_by_name("text_in_shadow_root_name")
    assert "Inside a shadow root" == inner_element.value
