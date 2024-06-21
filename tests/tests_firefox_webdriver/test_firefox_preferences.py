import pytest


@pytest.fixture(scope="session")
def browser_kwargs():
    prefs = {
        "profile_preferences": {
            "dom.max_script_run_time": 213,
            "devtools.inspector.enabled": True,
        },
    }
    return prefs


def test_preference_set(request, browser):
    # Rip the preferences out of firefox's config page
    browser.visit("about:config")
    browser.find_by_id("warningButton").click()
    browser.find_by_id("about-config-search").fill("dom.max_script_run_time")
    elem = browser.find_by_xpath("//table[@id='prefs']/tr[1]/td[1]/span/span")
    assert elem.value == "213"
