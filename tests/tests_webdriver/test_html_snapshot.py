import os
import tempfile

from tests.fake_webapp import EXAMPLE_APP


def test_take_snapshot_no_unique_file(browser):
    """When the unique_file parameter is false,
    Then the filename should match the name parameter exactly.
    """
    browser.visit(EXAMPLE_APP)
    browser.html_snapshot(name="test_html_snap", unique_file=False)

    expected_filepath = os.path.abspath("test_html_snap.html")
    assert os.path.isfile(expected_filepath)


def test_html_snapshot(browser):
    """Should take an html snapshot of the current page."""
    browser.visit(EXAMPLE_APP)

    filename = browser.html_snapshot()
    assert tempfile.gettempdir() in filename


def test_html_snapshot_with_prefix(browser):
    """Should add the prefix to the snapshot filename"""
    browser.visit(EXAMPLE_APP)

    filename = browser.html_snapshot(name="foobar")
    assert "foobar" in filename


def test_html_snapshot_with_suffix(browser):
    """Should add the suffix to the snapshot filename"""
    browser.visit(EXAMPLE_APP)

    filename = browser.html_snapshot(suffix="xml")
    assert "xml" == filename[-3:]
