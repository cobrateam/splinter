def test_keyboard_down_modifier(browser, app_url):
    """Scenario: Keys can be held down"""
    browser.visit(app_url)

    browser.keyboard.down("CONTROL")

    elem = browser.find_by_css("#keypress_detect")
    assert elem.first


def test_keyboard_up_modifier(browser, app_url):
    """Scenario: Keys can be held up"""
    browser.visit(app_url)

    browser.keyboard.down("CONTROL")
    browser.keyboard.up("CONTROL")

    elem = browser.find_by_css("#keyup_detect")
    assert elem.first


def test_keyboard_press_modifier(browser, app_url):
    """Scenario: Keys can be pressed"""
    browser.visit(app_url)

    browser.keyboard.press("CONTROL")

    elem = browser.find_by_css("#keyup_detect")
    assert elem.first


def test_element_press_combo(browser, app_url):
    """Scenario: Key presses can be used in a combo"""
    browser.visit(app_url)

    browser.keyboard.press("CONTROL+a")

    elem = browser.find_by_css("#keypress_detect_a")
    assert elem.first


def test_keyboard_pressed_modifier(browser, app_url):
    """Scenario: Keys can be pressed by a context manager."""
    browser.visit(app_url)

    with browser.keyboard.pressed("CONTROL"):
        down_elem = browser.find_by_css("#keypress_detect")
        assert down_elem.first

        up_elem = browser.find_by_css("#keyup_detect")
        assert up_elem.is_empty()

    up_elem = browser.find_by_css("#keyup_detect")
    assert up_elem.first


def test_keyboard_ctrl(browser, app_url):
    """Scenario: The CTRL value is correct across platforms"""
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
