def test_can_open_page(browser, app_url):
    """should be able to visit, get title and quit"""
    browser.visit(app_url)
    assert "Example Title" == browser.title


def test_should_reload_a_page(browser, app_url):
    browser.visit(app_url)
    browser.reload()
    assert "Example Title" == browser.title


def test_can_back_on_history(browser, app_url):
    """should be able to back on history"""
    browser.visit(app_url)
    browser.visit(f"{app_url}iframe")
    browser.back()
    assert app_url == browser.url


def test_can_forward_on_history(request, browser, app_url):
    """User can forward history"""
    request.addfinalizer(browser.quit)

    next_url = f"{app_url}iframe"

    browser.visit(app_url)
    browser.visit(next_url)
    browser.back()

    browser.forward()
    assert next_url == browser.url


def test_redirection(browser, app_url):
    """
    when visiting /redirected, browser should be redirected to /redirected-location?come=get&some=true
    browser.url should be updated
    """
    browser.visit(f"{app_url}redirected")
    assert "I just been redirected to this location." in browser.html
    assert "redirect-location?come=get&some=true" in browser.url
