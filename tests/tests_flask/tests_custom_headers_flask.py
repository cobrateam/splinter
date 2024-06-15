import pytest

from tests.fake_webapp import app


@pytest.fixture()
def browser_kwargs():
    return {
        "app": app,
        "wait_time": 0.1,
        "custom_headers": {
            "X-Splinter-Customheaders-1": "Hello",
            "X-Splinter-Customheaders-2": "Bye",
        },
    }


def test_create_a_flask_client_with_custom_headers(request, browser, app_url):
    request.addfinalizer(browser.quit)

    browser.visit(app_url + "headers")
    assert browser.is_text_present("X-Splinter-Customheaders-1: Hello")
    assert browser.is_text_present("X-Splinter-Customheaders-2: Bye")
