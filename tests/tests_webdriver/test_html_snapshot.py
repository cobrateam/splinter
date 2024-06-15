import os
import tempfile


def test_take_snapshot_no_unique_file(browser, app_url):
    """When the unique_file parameter is false,
    Then the filename should match the name parameter exactly.
    """
    browser.visit(app_url)
    browser.html_snapshot(name="test_html_snap", unique_file=False)

    expected_filepath = os.path.abspath("test_html_snap.html")
    assert os.path.isfile(expected_filepath)


def test_html_snapshot(browser, app_url):
    """Should take an html snapshot of the current page."""
    browser.visit(app_url)

    filename = browser.html_snapshot()
    assert tempfile.gettempdir() in filename


def test_html_snapshot_with_prefix(browser, app_url):
    """Should add the prefix to the snapshot filename"""
    browser.visit(app_url)

    filename = browser.html_snapshot(name="foobar")
    assert "foobar" in filename


def test_html_snapshot_with_suffix(browser, app_url):
    """Should add the suffix to the snapshot filename"""
    browser.visit(app_url)

    filename = browser.html_snapshot(suffix="xml")
    assert "xml" == filename[-3:]
