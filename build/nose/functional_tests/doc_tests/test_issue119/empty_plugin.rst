Minimal plugin
--------------

Plugins work as long as they implement the minimal interface required
by nose.plugins.base. They do not have to derive from
nose.plugins.Plugin.

    >>> class NullPlugin(object):
    ...
    ...     enabled = True
    ...     name = "null"
    ...     score = 100
    ...
    ...     def options(self, parser, env):
    ...         pass
    ...
    ...     def configure(self, options, conf):
    ...         pass
    >>> import unittest
    >>> from nose.plugins.plugintest import run_buffered as run
    >>> run(suite=unittest.TestSuite(tests=[]),
    ...     plugins=[NullPlugin()]) # doctest: +REPORT_NDIFF
    ----------------------------------------------------------------------
    Ran 0 tests in ...s
    <BLANKLINE>
    OK

Plugins can derive from nose.plugins.base and do nothing except set a
name.

    >>> import os
    >>> from nose.plugins import Plugin
    >>> class DerivedNullPlugin(Plugin):
    ...
    ...     name = "derived-null"

Enabled plugin that's otherwise empty

    >>> class EnabledDerivedNullPlugin(Plugin):
    ...
    ...     enabled = True
    ...     name = "enabled-derived-null"
    ...
    ...     def options(self, parser, env=os.environ):
    ...         pass
    ...
    ...     def configure(self, options, conf):
    ...         if not self.can_configure:
    ...             return
    ...         self.conf = conf
    >>> run(suite=unittest.TestSuite(tests=[]),
    ...     plugins=[DerivedNullPlugin(), EnabledDerivedNullPlugin()])
    ...     # doctest: +REPORT_NDIFF
    ----------------------------------------------------------------------
    Ran 0 tests in ...s
    <BLANKLINE>
    OK
