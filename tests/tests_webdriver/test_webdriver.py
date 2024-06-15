import os
import pathlib

import pytest


xfail_if_safari = pytest.mark.xfail(
    os.getenv("SAFARI"),
    reason="Safari issues need to be investigated.",
)


def test_default_wait_time(browser):
    "should driver default wait time 2"
    assert 2 == browser.wait_time


def test_status_code(browser):
    with pytest.raises(NotImplementedError):
        browser.status_code


def test_can_open_page_in_new_tab(browser, app_url):
    """should be able to visit url in a new tab"""
    browser.visit(app_url)
    browser.windows.current.new_tab(app_url)
    browser.windows[1].is_current = True
    assert app_url == browser.url
    assert 2 == len(browser.windows)

    browser.windows[0].is_current = True
    browser.windows[1].close()


@xfail_if_safari
def test_attach_file(request, browser, app_url):
    """Should provide a way to change file field value"""
    file_path = pathlib.Path(
        os.getcwd(),  # NOQA PTH109
        "tests",
        "mockfile.txt",
    )

    browser.visit(app_url)
    browser.attach_file("file", str(file_path))
    browser.find_by_name("upload").click()

    html = browser.html
    assert "text/plain" in html

    with open(file_path) as f:
        assert str(f.read()) in html


def test_browser_config(request, browser_name, browser_kwargs):
    """Splinter's drivers get the Config object when it's passed through the Browser function."""
    from splinter import Config
    from splinter import Browser

    config = Config(user_agent="agent_smith", headless=True)
    browser = Browser(browser_name, config=config, **browser_kwargs)
    request.addfinalizer(browser.quit)

    assert browser.config.user_agent == "agent_smith"
