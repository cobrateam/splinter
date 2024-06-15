def test_can_clear_text_field_content(browser, app_url):
    browser.visit(app_url)
    my_input = "random query"
    elem = browser.find_by_name("query")
    elem.fill(my_input)
    assert my_input == elem.value

    elem.clear()
    assert not elem.value


def test_can_clear_password_field_content(browser, app_url):
    browser.visit(app_url)
    my_input = "1nF4m310"
    elem = browser.find_by_name("password")
    elem.fill(my_input)
    assert my_input == elem.value

    elem.clear()
    assert not elem.value


def test_can_clear_tel_field_content(browser, app_url):
    browser.visit(app_url)
    my_input = "5553743980"
    elem = browser.find_by_name("telephone")
    elem.fill(my_input)
    assert my_input == elem.value

    elem.clear()
    assert not elem.value


def test_can_clear_textarea_content(browser, app_url):
    browser.visit(app_url)
    elem = browser.find_by_name("description")
    elem.fill("A box of widgets")
    assert "A box of widgets" == elem.value

    elem.clear()
    assert "" == elem.value


def test_can_clear_search_content(browser, app_url):
    browser.visit(app_url)
    elem = browser.find_by_name("search_keyword")
    elem.fill("widgets")
    assert "widgets" == elem.value

    elem.clear()
    assert "" == elem.value


def test_can_clear_url_content(browser, app_url):
    browser.visit(app_url)
    elem = browser.find_by_name("url_input")
    elem.fill("http://widgets.com")
    assert "http://widgets.com" == elem.value

    elem.clear()
    assert "" == elem.value
