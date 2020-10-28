import pluggy

from splinter import hookspecs


hookimpl = pluggy.HookimplMarker('splinter')

plugins = pluggy.PluginManager('splinter')
plugins.add_hookspecs(hookspecs)
