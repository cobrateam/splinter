import time


def test_cookies_extra_parameters(browser, app_url):
    """Cookie can be created with extra parameters."""
    browser.visit(app_url)
    timestamp = int(time.time() + 120)
    browser.cookies.add({"sha": "zam"}, expiry=timestamp)
    cookie = browser.driver.get_cookie("sha")
    assert timestamp == cookie["expiry"]
