import pytest


def test_can_clear_text_field_content(browser, app_url):
    """lxml-based drivers should not be able to clear"""
    browser.visit(app_url)
    with pytest.raises(NotImplementedError):
        browser.find_by_name("query").first.clear()


def test_can_clear_password_field_content(browser, app_url):
    """lxml-based drivers should not be able to clear"""
    browser.visit(app_url)
    with pytest.raises(NotImplementedError):
        browser.find_by_name("password").first.clear()


def test_can_clear_tel_field_content(browser, app_url):
    """lxml-based drivers should not be able to clear"""
    browser.visit(app_url)
    with pytest.raises(NotImplementedError):
        browser.find_by_name("telephone").first.clear()


def test_can_clear_textarea_content(browser, app_url):
    """lxml-based drivers should not be able to clear"""
    browser.visit(app_url)
    with pytest.raises(NotImplementedError):
        browser.find_by_name("description").first.clear()


def test_can_clear_search_content(browser, app_url):
    """lxml-based drivers should not be able to clear"""
    browser.visit(app_url)
    with pytest.raises(NotImplementedError):
        browser.find_by_name("search_keyword").first.clear()


def test_can_clear_url_content(browser, app_url):
    """lxml-based drivers should not be able to clear"""
    browser.visit(app_url)
    with pytest.raises(NotImplementedError):
        browser.find_by_name("url_input").first.clear()
