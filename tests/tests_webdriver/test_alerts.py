import time


def test_access_alerts_and_accept_them(browser, app_url):
    browser.visit(app_url + "alert")
    browser.find_by_tag("h1").click()
    alert = browser.get_alert()
    assert "This is an alert example." == alert.text
    alert.accept()


def test_access_prompts_and_be_able_to_fill_then(browser, app_url):
    browser.visit(app_url + "alert")
    browser.find_by_tag("h2").click()

    alert = browser.get_alert()
    assert "What is your name?" == alert.text
    alert.fill_with("Splinter")
    alert.accept()

    # Wait for alert
    time.sleep(2.5)

    response = browser.get_alert()
    assert "Splinter" == response.text
    response.accept()


def test_access_confirm_and_accept_and_dismiss_them(browser, app_url):
    browser.visit(app_url + "alert")

    browser.find_by_tag("h3").click()
    alert = browser.get_alert()

    assert "Should I continue?" == alert.text
    alert.accept()

    # Wait for alert
    time.sleep(2.5)

    alert = browser.get_alert()
    assert "You say I should" == alert.text
    alert.accept()

    browser.find_by_tag("h3").click()
    alert = browser.get_alert()
    assert "Should I continue?" == alert.text
    alert.dismiss()

    # Wait for alert
    time.sleep(2.5)

    alert = browser.get_alert()
    assert "You say I should not" == alert.text
    alert.accept()


def test_access_confirm_and_accept_and_dismiss_them_using_with(browser, app_url):
    browser.visit(app_url + "alert")

    browser.find_by_tag("h3").click()
    with browser.get_alert() as alert:
        assert "Should I continue?" == alert.text
        alert.accept()

    # Wait for alert
    time.sleep(2.5)

    with browser.get_alert() as alert:
        assert "You say I should" == alert.text
        alert.accept()

    browser.find_by_tag("h3").click()
    with browser.get_alert() as alert:
        assert "Should I continue?" == alert.text
        alert.dismiss()

    # Wait for alert
    time.sleep(2.5)

    with browser.get_alert() as alert:
        assert "You say I should not" == alert.text
        alert.accept()


def test_access_alerts_using_with(browser, app_url):
    "should access alerts using 'with' statement"
    browser.visit(app_url + "alert")
    browser.find_by_tag("h1").click()
    with browser.get_alert() as alert:
        assert "This is an alert example." == alert.text
        alert.accept()


def test_get_alert_return_none_if_no_alerts(browser, app_url):
    "should return None if no alerts available"
    alert = browser.get_alert()
    assert alert is None
