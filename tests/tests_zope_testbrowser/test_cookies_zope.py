def test_cookies_extra_parameters(browser, app_url):
    """Cookie can be created with extra parameters."""
    browser.visit(app_url)
    comment = "Ipsum lorem"
    browser.cookies.add({"sha": "zam"}, comment=comment)
    cookie = browser._browser.cookies.getinfo("sha")
    assert "Ipsum%20lorem" == cookie["comment"]
