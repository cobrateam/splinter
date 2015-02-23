import warnings


def warn_deprecated(method, deprecated_method_name):
    def deprecated_method(*args, **kwargs):
        warnings.warn(
            "'%s' is deprecated, use '%s' instead." % (deprecated_method_name, method.__name__),
            DeprecationWarning,
            stacklevel=2
        )
        return method(*args, **kwargs)
    return deprecated_method
