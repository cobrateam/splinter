import os
import pathlib

import pytest


def test_cant_switch_to_frame(browser, app_url):
    """lxml-based drivers should not be able to switch to frames"""
    browser.visit(app_url)
    with pytest.raises(NotImplementedError) as err:
        browser.get_iframe("frame_123")
        browser.fail()

    assert f"{browser.driver_name.lower()} doesn't support frames." == err.value.args[0]


def test_attach_file(browser, app_url):
    """should provide a way to change file field value"""
    browser.visit(app_url)

    file_path = pathlib.Path(
        os.getcwd(),  # NOQA PTH109
        "tests",
        "mockfile.txt",
    )

    browser.attach_file("file", str(file_path))
    browser.find_by_name("upload").click()

    html = browser.html
    assert "text/plain" in html
    with open(file_path) as f:
        assert f.read() in html


def test_forward_to_none_page(request, browser, app_url):
    """lxml-based drivers should not fail when trying to forward to none"""
    request.addfinalizer(browser.quit)

    browser.visit(app_url)
    browser.forward()
    assert app_url == browser.url


def test_cant_mouseover(browser, app_url):
    """lxml-based drivers should not be able to put the mouse over the element"""
    browser.visit(app_url)
    with pytest.raises(NotImplementedError):
        browser.find_by_css("#visible").mouse_over()


def test_cant_mouseout(browser, app_url):
    """lxml-based drivers should not be able to mouse out of an element"""
    browser.visit(app_url)
    with pytest.raises(NotImplementedError):
        browser.find_by_css("#visible").mouse_out()


def test_finding_all_links_by_non_ascii_text(browser, app_url):
    """lxml-based drivers should find links by non ascii text"""
    non_ascii_encodings = {
        "pangram_pl": "Jeżu klątw, spłódź Finom część gry hańb!",
        "pangram_ja": "天 地 星 空",
        "pangram_ru": "В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!",  # NOQA RUF001
        "pangram_eo": "Laŭ Ludoviko Zamenhof bongustas freŝa ĉeĥa manĝaĵo kun spicoj.",
    }
    browser.visit(app_url)
    for key, text in non_ascii_encodings.items():
        link = browser.links.find_by_text(text)
        assert key == link["id"]


def test_links_with_nested_tags_xpath(browser, app_url):
    browser.visit(app_url)
    links = browser.find_by_xpath('//a/span[text()="first bar"]/..')
    assert len(links) == 1, 'Found more than one link with a span with text "BAR ONE". %s' % [
        item.outer_html for item in links
    ]
