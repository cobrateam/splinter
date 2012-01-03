import warnings


def warn_deprecated(method, deprecated_method_name):
    def deprecated_method(*args, **kwargs):
        warnings.warn("'%s' is deprecated, use '%s' instead." % (deprecated_method_name, method.__name__), DeprecationWarning, stacklevel=2)
        return method(*args, **kwargs)
    return deprecated_method


def deprecate_driver_class(cls, message):
    def new_init(self, *args, **kwargs):
        cls.__init__(self, *args, **kwargs)
        warnings.warn(message, DeprecationWarning, stacklevel=3)

    cls_dict = dict(cls.__dict__)
    cls_dict['__init__'] = new_init
    return type("Deprecated%s" % cls.__name__, (cls,), cls_dict)
