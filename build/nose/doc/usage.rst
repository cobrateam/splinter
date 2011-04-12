Basic usage
-----------

Use the nosetests script (after installation by setuptools)::

  nosetests [options] [(optional) test files or directories]

In addition to passing command-line options, you may also put configuration
options in a .noserc or nose.cfg file in your home directory. These are
standard .ini-style config files. Put your nosetests configuration in a
[nosetests] section, with the -- prefix removed::

   [nosetests]
   verbosity=3
   with-doctest=1
  
There are several other ways to use the nose test runner besides the
`nosetests` script. You may use nose in a test script::

  import nose
  nose.main()

If you don't want the test script to exit with 0 on success and 1 on failure
(like unittest.main), use nose.run() instead::

  import nose
  result = nose.run()
  
`result` will be true if the test run succeeded, or false if any test failed
or raised an uncaught exception. Lastly, you can run nose.core directly, which
will run nose.main()::

  python /path/to/nose/core.py
  
Please see the usage message for the nosetests script for information
about how to control which tests nose runs, which plugins are loaded,
and the test output.

Extended usage
^^^^^^^^^^^^^^

.. autohelp ::
