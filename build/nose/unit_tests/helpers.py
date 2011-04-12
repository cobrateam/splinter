def iter_compat(suite):
    try:
        suite.__iter__
        return suite
    except AttributeError:
        return suite._tests
