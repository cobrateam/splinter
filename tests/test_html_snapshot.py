import os
import tempfile

from .base import supported_browsers
from .fake_webapp import EXAMPLE_APP

import pytest


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_take_snapshot_no_unique_file(get_new_browser, browser_name):
    """When the unique_file parameter is false,
    Then the filename should match the name parameter exactly.
    """
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)
    browser.html_snapshot(name='test_html_snap', unique_file=False)

    expected_filepath = os.path.abspath('test_html_snap.html')
    assert os.path.isfile(expected_filepath)


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_html_snapshot(get_new_browser, browser_name):
    """Should take an html snapshot of the current page."""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    filename = browser.html_snapshot()
    assert tempfile.gettempdir() in filename


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_html_snapshot_with_prefix(get_new_browser, browser_name):
    """Should add the prefix to the snapshot filename"""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    filename = browser.html_snapshot(name="foobar")
    assert "foobar" in filename


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_html_snapshot_with_suffix(get_new_browser, browser_name):
    """Should add the suffix to the snapshot filename"""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    filename = browser.html_snapshot(suffix="xml")
    assert "xml" == filename[-3:]
