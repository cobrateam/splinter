Cover: code coverage
====================

.. note ::

   Newer versions of coverage contain their own nose plugin which is
   superior to the builtin plugin. It exposes more of coverage's
   options and uses coverage's native html output. Depending on the
   version of coverage installed, the included plugin may override the
   nose builtin plugin, or be available under a different name. Check
   ``nosetests --help`` or ``nosetests --plugins`` to find out which
   coverage plugin is available on your system.

.. autoplugin :: nose.plugins.cover
