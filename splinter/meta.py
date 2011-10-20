# -*- coding: utf-8 -*-

class InheritedDocs(type):

    def __new__(mcs, class_name, bases, dict):
        docstring = dict.get('__doc__', None)

        items_to_patch = [(k, v) for k, v in dict.items() if not k.startswith('__') and not v.__doc__]
        for name, obj in items_to_patch:
            doc = None
            for base in bases:
                if hasattr(base, name):
                    doc = getattr(base, name).__doc__

                    if doc:
                        if type(obj) == type(property()) and not obj.fset:
                            obj.fget.__doc__ = doc
                            dict[name] = property(fget=obj.fget)
                        else:
                            obj.__doc__ = doc
                        break

        return type.__new__(mcs, class_name, bases, dict)
