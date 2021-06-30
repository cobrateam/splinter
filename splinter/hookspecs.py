import pluggy


hookspec = pluggy.HookspecMarker('splinter')


@hookspec
def splinter_after_visit(browser):
    """Is run after browser.visit()

    Arguments:
        browser (Browser): Current browser instance.
    """
    pass


@hookspec
def splinter_before_quit(browser):
    """Is run before browser.quit().

    Arguments:
        browser (Browser): Current browser instance.
    """
    pass


@hookspec
def splinter_prepare_drivers(drivers):
    # type(Dict[str, Callable]) -> Dict[str, Callable]
    """Called before a driver is initialized.

    Arguments:
        drivers: Dict containing name: driver mappings
    """
    pass
