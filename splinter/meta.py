# -*- coding: utf-8 -*-

class InheritedDocs(type):

    def __new__(mcs, name, bases, dict):
        docstring = dict.get('__doc__', None)

        items_to_patch = [(k, v) for k, v in dict.items() if not k.startswith('__') and not v.__doc__]
        for name, obj in items_to_patch:
            doc = None
            for base in bases:
                if hasattr(base, name):
                    doc = getattr(base, name).__doc__

                    if doc:
                        obj.__doc__ = doc
                        break

        return type.__new__(mcs, name, bases, dict)
