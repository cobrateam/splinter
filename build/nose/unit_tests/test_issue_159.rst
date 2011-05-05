    >>> from nose.plugins.errorclass import ErrorClass, ErrorClassPlugin
    >>> class X(Exception):
    ...     pass
    >>> xes = ErrorClass(X, label='XXX')
    Traceback (most recent call last):
    TypeError: 'isfailure' is a required named argument for ErrorClass
