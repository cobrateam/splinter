"""
Module with errors in doctest formatting.

    >>> 1
    'this is\n an error'
"""
def foo():
    pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()
