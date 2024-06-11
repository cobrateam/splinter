import platform

from splinter.driver.webdriver import Keyboard


def test_keyboard_down_modifier(browser, app_url):
    browser.visit(app_url)

    keyboard = Keyboard(browser.driver)

    keyboard.down("CONTROL")

    elem = browser.find_by_css("#keypress_detect")
    assert elem.first


def test_keyboard_up_modifier(browser, app_url):
    browser.visit(app_url)

    keyboard = Keyboard(browser.driver)

    keyboard.down("CONTROL")
    keyboard.up("CONTROL")

    elem = browser.find_by_css("#keyup_detect")
    assert elem.first


def test_keyboard_press_modifier(browser, app_url):
    browser.visit(app_url)

    keyboard = Keyboard(browser.driver)

    keyboard.press("CONTROL")

    elem = browser.find_by_css("#keyup_detect")
    assert elem.first


def test_element_press_combo(browser, app_url):
    browser.visit(app_url)

    keyboard = Keyboard(browser.driver)

    keyboard.press("CONTROL+a")

    elem = browser.find_by_css("#keypress_detect_a")
    assert elem.first


def test_element_copy_paste(browser, app_url):
    control_key = "META" if platform.system() == "Darwin" else "CONTROL"

    browser.visit(app_url)

    elem = browser.find_by_name("q")
    elem.fill("Copy this value")
    elem.press(f"{control_key}+a")
    elem.press(f"{control_key}+c")
    elem.clear()

    assert elem.first.value == ""

    elem.press(f"{control_key}+v")

    assert elem.first.value == "Copy this Value"
