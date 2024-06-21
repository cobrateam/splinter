import pytest


@pytest.fixture(scope="session")
def browser_kwargs():
    return {"capabilities": {"pageLoadStrategy": "eager"}}


def test_capabilities_set(request, browser):
    capabilities = browser.driver.capabilities
    assert "pageLoadStrategy" in capabilities
    assert "eager" == capabilities.get("pageLoadStrategy")
