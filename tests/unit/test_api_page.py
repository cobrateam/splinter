from splinter.page import Page
from ludibrio import Stub


def test_page_should_have_title():
    with Stub() as driver:
        driver.title >> 'foo title'
    page = Page('http://example.com', driver)
    assert page.title == 'foo title'
