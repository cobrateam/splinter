from splinter.driver.webdriver import Keyboard


def test_keyboard_down_modifier(browser, app_url):
    browser.visit(app_url)

    keyboard = Keyboard(browser.driver)

    keyboard.down("CTRL")

    elem = browser.find_by_css("#keypress_detect")
    assert elem.first


def test_keyboard_up_modifier(browser, app_url):
    browser.visit(app_url)

    keyboard = Keyboard(browser.driver)

    keyboard.down("CTRL")
    keyboard.up("CTRL")

    elem = browser.find_by_css("#keyup_detect")
    assert elem.first


def test_keyboard_press_modifier(browser, app_url):
    browser.visit(app_url)

    keyboard = Keyboard(browser.driver)

    keyboard.press("CTRL")

    elem = browser.find_by_css("#keyup_detect")
    assert elem.first


def test_element_press_combo(browser, app_url):
    browser.visit(app_url)

    keyboard = Keyboard(browser.driver)

    keyboard.press("CTRL+a")

    elem = browser.find_by_css("#keypress_detect_a")
    assert elem.first


def test_keyboard_copy_paste(browser, app_url):
    browser.visit(app_url)

    elem_with_value_to_copy = browser.find_by_css("input[name='q']").first
    elem_to_paste_into = browser.find_by_css("input[name='telephone']").first

    elem_with_value_to_copy.fill("Copy this value")

    browser.keyboard.press("CTRL+a")
    browser.keyboard.press("CTRL+c")

    assert elem_to_paste_into.value == ""

    elem_to_paste_into.click()

    browser.keyboard.press("CTRL+v")
    assert elem_to_paste_into.value == "Copy this value"
