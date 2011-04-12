Importing Tests
---------------

When a package imports tests from another package, the tests are
**completely** relocated into the importing package. This means that the
fixtures from the source package are **not** run when the tests in the
importing package are executed.

For example, consider this collection of packages:

    >>> import os
    >>> support = os.path.join(os.path.dirname(__file__), 'support')
    >>> from nose.util import ls_tree
    >>> print ls_tree(support) # doctest: +REPORT_NDIFF
    |-- package1
    |   |-- __init__.py
    |   `-- test_module.py
    |-- package2c
    |   |-- __init__.py
    |   `-- test_module.py
    `-- package2f
        |-- __init__.py
        `-- test_module.py

In these packages, the tests are all defined in package1, and are imported
into package2f and package2c.

.. Note ::

   The run() function in :mod:`nose.plugins.plugintest` reformats test result
   output to remove timings, which will vary from run to run, and
   redirects the output to stdout.

    >>> from nose.plugins.plugintest import run_buffered as run

..

package1 has fixtures, which we can see by running all of the tests. Note
below that the test names reflect the modules into which the tests are
imported, not the source modules.

    >>> argv = [__file__, '-v', support]
    >>> run(argv=argv) # doctest: +REPORT_NDIFF
    package1 setup
    test (package1.test_module.TestCase) ... ok
    package1.test_module.TestClass.test_class ... ok
    package1.test_module.test_function ... ok
    package2c setup
    test (package2c.test_module.TestCase) ... ok
    package2c.test_module.TestClass.test_class ... ok
    package2f setup
    package2f.test_module.test_function ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 6 tests in ...s
    <BLANKLINE>
    OK

When tests are run in package2f or package2c, only the fixtures from those
packages are executed.

    >>> argv = [__file__, '-v', os.path.join(support, 'package2f')]
    >>> run(argv=argv) # doctest: +REPORT_NDIFF
    package2f setup
    package2f.test_module.test_function ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    OK
    >>> argv = [__file__, '-v', os.path.join(support, 'package2c')]
    >>> run(argv=argv) # doctest: +REPORT_NDIFF
    package2c setup
    test (package2c.test_module.TestCase) ... ok
    package2c.test_module.TestClass.test_class ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 2 tests in ...s
    <BLANKLINE>
    OK

This also applies when only the specific tests are selected via the
command-line.

    >>> argv = [__file__, '-v',
    ...         os.path.join(support, 'package2c', 'test_module.py') +
    ...         ':TestClass.test_class']
    >>> run(argv=argv) # doctest: +REPORT_NDIFF
    package2c setup
    package2c.test_module.TestClass.test_class ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    OK
    >>> argv = [__file__, '-v',
    ...         os.path.join(support, 'package2c', 'test_module.py') +
    ...         ':TestCase.test']
    >>> run(argv=argv) # doctest: +REPORT_NDIFF
    package2c setup
    test (package2c.test_module.TestCase) ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    OK
    >>> argv = [__file__, '-v',
    ...         os.path.join(support, 'package2f', 'test_module.py') +
    ...         ':test_function']
    >>> run(argv=argv) # doctest: +REPORT_NDIFF
    package2f setup
    package2f.test_module.test_function ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    OK
