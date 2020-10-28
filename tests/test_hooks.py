from .base import get_browser
from .fake_webapp import EXAMPLE_APP

import splinter


class DummyPlugin:
    """Bare bones dummy pluggin."""
    @splinter.hookimpl
    def splinter_after_visit(self, browser):
        return 'after visit'

    @splinter.hookimpl
    def splinter_before_quit(self, browser):
        return 'before quit'


class DummyPlugin2:
    """Dummy plugin with effects that can be seen."""
    @splinter.hookimpl
    def splinter_after_visit(self, browser):
        browser.execute_script('document.foo = "after visit"')

    @splinter.hookimpl
    def splinter_before_quit(self, browser):
        splinter.foo = 'bar'


splinter.plugins.register(DummyPlugin())
splinter.plugins.register(DummyPlugin2())


def test_splinter_after_visit_register(request):
    """Hook should be registered."""

    browser = get_browser('chrome')
    request.addfinalizer(browser.quit)

    results = browser.hook.splinter_after_visit(browser=browser)

    assert ['after visit'] == results


def test_splinter_before_quit_register(request):
    """Hook should be registered."""

    browser = get_browser('chrome')
    request.addfinalizer(browser.quit)

    results = browser.hook.splinter_before_quit(browser=browser)

    assert ['before quit'] == results


def test_splinter_after_visit(request):
    """Hooks should run correctly."""

    browser = get_browser('chrome')
    request.addfinalizer(browser.quit)

    browser.visit(EXAMPLE_APP)

    result = browser.evaluate_script("document.foo")

    assert 'after visit' == result


def test_splinter_before_quit(request):
    """Hooks should run correctly."""

    browser = get_browser('chrome')
    browser.quit()

    assert splinter.foo == 'bar'
