import pytest

from selenium.common.exceptions import JavascriptException


def test_execute_script_valid(browser, app_url):
    """Scenario: Execute Valid JavaScript

    When I execute valid JavaScript code which modifies the DOM
    Then the modifications are seen in the document
    """
    browser.visit(app_url)

    browser.execute_script("document.querySelector('body').innerHTML = ''")

    elem = browser.find_by_tag("body").first
    assert elem.value == ""


def test_execute_script_return_value(browser, app_url):
    """Scenario: Execute Valid JavaScript With No Return Value

    When I execute valid JavaScript code
    And the code does not return a value
    Then no value is returned to the driver
    """
    browser.visit(app_url)

    result = browser.execute_script("document.querySelector('body').innerHTML")
    assert result is None


def test_execute_script_return_value_if_explicit(browser):
    """Scenario: Execute Valid JavaScript With A Return Value

    When I execute JavaScript code
    And the code returns a value
    Then the value is returned from the web browser
    """
    result = browser.execute_script("return 42")
    assert result == 42


def test_execute_script_valid_args(browser, app_url):
    """Scenario: Execute Valid JavaScript With Arguments

    When I execute valid JavaScript code which modifies the DOM
    And I send arguments to the web browser
    Then the arguments are available for use
    """
    browser.visit(app_url)

    browser.execute_script(
        "document.querySelector('body').innerHTML = arguments[0] + arguments[1]",
        "A String And ",
        "Another String",
    )

    elem = browser.find_by_tag("body").first
    assert elem.value == "A String And Another String"


def test_execute_script_valid_args_element(browser, app_url):
    """Scenario: Execute Valid JavaScript With Arguments - Send Element

    When I execute valid JavaScript code
    And I send an Element to the web browser as an argument
    Then the argument is available for use
    """
    browser.visit(app_url)

    elem = browser.find_by_id("firstheader").first
    assert elem.value == "Example Header"
    browser.execute_script("arguments[0].innerHTML = 'A New Header'", elem)

    elem = browser.find_by_id("firstheader").first
    assert elem.value == "A New Header"


def test_execute_script_invalid(browser, app_url):
    """Scenario: Evaluate Invalid JavaScript

    When I execute invalid JavaScript code
    Then an error is raised
    """
    browser.visit(app_url)

    with pytest.raises(JavascriptException):
        browser.execute_script("invalid.thisIsNotGood()")


def test_execute_script_invalid_args(browser, app_url):
    """Scenario: Execute Valid JavaScript With Invalid Arguments

    When I execute valid JavaScript code which modifies the DOM
    And I send an object to the browser which is not JSON serializable
    Then an error is raised
    """
    browser.visit(app_url)

    def unserializable():
        "You can't JSON serialize a function."

    with pytest.raises(TypeError):
        browser.execute_script("arguments[0]", unserializable)
