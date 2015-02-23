# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class InheritedDocs(type):

    def __new__(mcs, class_name, bases, dict):
        items_to_patch = [(k, v) for k, v in dict.items()
                          if not k.startswith('__') and not v.__doc__]
        for name, obj in items_to_patch:
            doc = None
            for base in bases:
                if hasattr(base, name):
                    doc = getattr(base, name).__doc__

                    if doc:
                        if isinstance(obj, property) and not obj.fset:
                            obj.fget.__doc__ = doc
                            dict[name] = property(fget=obj.fget)
                        else:
                            obj.__doc__ = doc
                        break

        return type.__new__(mcs, class_name, bases, dict)
