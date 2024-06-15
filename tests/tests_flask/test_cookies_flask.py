import time


def test_cookies_extra_parameters(browser):
    """Cookie can be created with extra parameters."""
    timestamp = int(time.time() + 120)
    browser.cookies.add({"sha": "zam"}, expires=timestamp)
    cookie = {c.key: c for c in browser._browser._cookies.values()}["sha"]
    assert timestamp == int(cookie.expires.timestamp())
