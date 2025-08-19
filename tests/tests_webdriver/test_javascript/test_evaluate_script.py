import pytest

from selenium.common.exceptions import JavascriptException


def test_evaluate_script_valid(browser, app_url):
    """Scenario: Evaluating JavaScript Returns The Code's Result

    When I evaluate JavaScript code
    Then the result of the evaluation is returned
    """
    browser.visit(app_url)

    document_href = browser.evaluate_script("document.location.href")
    assert app_url == document_href


def test_evaluate_script_valid_args(browser, app_url):
    """Scenario: Execute Valid JavaScript With Arguments

    When I execute valid JavaScript code which modifies the DOM
    And I send arguments to the web browser
    Then the arguments are available for use
    """
    browser.visit(app_url)

    browser.evaluate_script(
        "document.querySelector('body').innerHTML = arguments[0] + arguments[1]",
        "A String And ",
        "Another String",
    )

    elem = browser.find_by_tag("body").first
    assert elem.value == "A String And Another String"


def test_evaluate_script_valid_args_element(browser, app_url):
    """Scenario: Execute Valid JavaScript

    When I execute valid JavaScript code
    And I send an Element to the browser as an argument
    Then the modifications are seen in the document
    """
    browser.visit(app_url)

    elem = browser.find_by_id("firstheader").first
    elem_text = browser.evaluate_script("arguments[0].innerHTML", elem)
    assert elem_text == "Example Header"


def test_evaluate_script_invalid(browser, app_url):
    """Scenario: Evaluate Invalid JavaScript.

    When I evaluate invalid JavaScript code
    Then an error is raised
    """
    browser.visit(app_url)

    with pytest.raises(JavascriptException):
        browser.evaluate_script("invalid.thisIsNotGood()")


def test_evaluate_script_invalid_args(browser, app_url):
    """Scenario: Execute Valid JavaScript

    When I execute valid JavaScript code which modifies the DOM
    And I send an object to the browser which is not JSON serializable
    Then an error is raised
    """
    browser.visit(app_url)

    def unserializable():
        "You can't JSON serialize a function."

    with pytest.raises(TypeError):
        browser.evaluate_script("arguments[0]", unserializable)
