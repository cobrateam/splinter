# Copyright 2016 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from splinter.browser import Browser  # NOQA

from splinter.plugin_manager import hookimpl, plugins

__version__ = "0.14.0"

__all__ = ['hookimpl', 'plugins']
