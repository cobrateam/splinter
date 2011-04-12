Parallel Testing with nose
--------------------------

.. Note ::

   Use of the multiprocess plugin on python 2.5 or earlier requires
   the multiprocessing_ module, available from PyPI and at
   http://code.google.com/p/python-multiprocessing/.

..

Using the `nose.plugin.multiprocess` plugin, you can parallelize a
test run across a configurable number of worker processes. While this can
speed up CPU-bound test runs, it is mainly useful for IO-bound tests
that spend most of their time waiting for data to arrive from someplace
else and can benefit from parallelization.

.. _multiprocessing : http://code.google.com/p/python-multiprocessing/

How tests are distributed
=========================

The ideal case would be to dispatch each test to a worker process separately,
and to have enough worker processes that the entire test run takes only as
long as the slowest test. This ideal is not attainable in all cases, however,
because many test suites depend on context (class, module or package)
fixtures.

Some context fixtures are re-entrant -- that is, they can be called many times
concurrently. Other context fixtures can be shared among tests running in
different processes. Still others must be run once and only once for a given
set of tests, and must be in the same process as the tests themselves.

The plugin can't know the difference between these types of context fixtures
unless you tell it, so the default behavior is to dispatch the entire context
suite to a worker as a unit. This way, the fixtures are run once, in the same
process as the tests. (That, of course, is how they are run when the plugin
is not active: All tests are run in a single process.)

Controlling distribution
^^^^^^^^^^^^^^^^^^^^^^^^

There are two context-level variables that you can use to control this default
behavior.

If a context's fixtures are re-entrant, set ``_multiprocess_can_split_ = True``
in the context, and the plugin will dispatch tests in suites bound to that
context as if the context had no fixtures. This means that the fixtures will
execute multiple times, typically once per test, and concurrently.

For example, a module that contains re-entrant fixtures might look like::

  _multiprocess_can_split_ = True

  def setup():
      ...

A class might look like::

  class TestClass:
      _multiprocess_can_split_ = True

      @classmethod
      def setup_class(cls):
          ...

Alternatively, If a context's fixtures may only be run once, or may not run
concurrently, but *may* be shared by tests running in different processes
-- for instance a package-level fixture that starts an external http server or
initializes a shared database -- then set ``_multiprocess_shared_ = True`` in
the context. Fixtures for contexts so marked will execute in the primary nose
process, and tests in those contexts will be individually dispatched to run in
parallel.

A module with shareable fixtures might look like::

  _multiprocess_shared_ = True

  def setup():
      ...

A class might look like::

  class TestClass:
      _multiprocess_shared_ = True

      @classmethod
      def setup_class(cls):
          ...

These options are mutually exclusive: you can't mark a context as both
splittable and shareable.

Example
~~~~~~~

Consider three versions of the same test suite. One
is marked ``_multiprocess_shared_``, another ``_multiprocess_can_split_``,
and the third is unmarked. They all define the same fixtures:

    called = []

    def setup():
        print "setup called"
        called.append('setup')

    def teardown():
        print "teardown called"
        called.append('teardown')

And each has two tests that just test that ``setup()`` has been called
once and only once.

When run without the multiprocess plugin, fixtures for the shared,
can-split and not-shared test suites execute at the same times, and
all tests pass.

.. Note ::

   The run() function in :mod:`nose.plugins.plugintest` reformats test result
   output to remove timings, which will vary from run to run, and
   redirects the output to stdout.

    >>> from nose.plugins.plugintest import run_buffered as run

..

    >>> import os
    >>> support = os.path.join(os.path.dirname(__file__), 'support')
    >>> test_not_shared = os.path.join(support, 'test_not_shared.py')
    >>> test_shared = os.path.join(support, 'test_shared.py')
    >>> test_can_split = os.path.join(support, 'test_can_split.py')

The module with shared fixtures passes.

    >>> run(argv=['nosetests', '-v', test_shared]) #doctest: +REPORT_NDIFF
    setup called
    test_shared.TestMe.test_one ... ok
    test_shared.test_a ... ok
    test_shared.test_b ... ok
    teardown called
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 3 tests in ...s
    <BLANKLINE>
    OK

As does the module with no fixture annotations.

    >>> run(argv=['nosetests', '-v', test_not_shared]) #doctest: +REPORT_NDIFF
    setup called
    test_not_shared.TestMe.test_one ... ok
    test_not_shared.test_a ... ok
    test_not_shared.test_b ... ok
    teardown called
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 3 tests in ...s
    <BLANKLINE>
    OK

And the module that marks its fixtures as re-entrant.

    >>> run(argv=['nosetests', '-v', test_can_split]) #doctest: +REPORT_NDIFF
    setup called
    test_can_split.TestMe.test_one ... ok
    test_can_split.test_a ... ok
    test_can_split.test_b ... ok
    teardown called
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 3 tests in ...s
    <BLANKLINE>
    OK

However, when run with the ``--processes=2`` switch, each test module
behaves differently.

    >>> from nose.plugins.multiprocess import MultiProcess

The module marked ``_multiprocess_shared_`` executes correctly, although as with
any use of the multiprocess plugin, the order in which the tests execute is
indeterminate.

First we have to reset all of the test modules.

    >>> import sys
    >>> sys.modules['test_not_shared'].called[:] = []
    >>> sys.modules['test_can_split'].called[:] = []

Then we can run the tests again with the multiprocess plugin active.
    
    >>> run(argv=['nosetests', '-v', '--processes=2', test_shared],
    ...     plugins=[MultiProcess()]) #doctest: +ELLIPSIS
    setup called
    test_shared.... ok
    teardown called
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 3 tests in ...s
    <BLANKLINE>
    OK

As does the one not marked -- however in this case, ``--processes=2``
will do *nothing at all*: since the tests are in a module with
unmarked fixtures, the entire test module will be dispatched to a
single runner process.

However, the module marked ``_multiprocess_can_split_`` will fail, since
the fixtures *are not reentrant*. A module such as this *must not* be
marked ``_multiprocess_can_split_``, or tests will fail in one or more
runner processes as fixtures are re-executed.

We have to reset all of the test modules again.

    >>> import sys
    >>> sys.modules['test_not_shared'].called[:] = []
    >>> sys.modules['test_can_split'].called[:] = []

Then we can run again and see the failures.

    >>> run(argv=['nosetests', '-v', '--processes=2', test_can_split],
    ...     plugins=[MultiProcess()]) #doctest: +ELLIPSIS
    test_can_split....
    ...
    FAILED (failures=...)

Other differences in test running
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The main difference between using the multiprocess plugin and not doing so
is obviously that tests run concurrently under multiprocess. However, there
are a few other differences that may impact your test suite:

* More tests may be found

  Because tests are dispatched to worker processes by name, a worker
  process may find and run tests in a module that would not be found during a
  normal test run. For instance, if a non-test module contains a test-like
  function, that function would be discovered as a test in a worker process
  if the entire module is dispatched to the worker. This is because worker
  processes load tests in *directed* mode -- the same way that nose loads
  tests when you explicitly name a module -- rather than in *discovered* mode,
  the mode nose uses when looking for tests in a directory.

* Out-of-order output

  Test results are collected by workers and returned to the master process for
  output. Since different processes may complete their tests at different
  times, test result output order is not determinate.

* Plugin interaction warning

  The multiprocess plugin does not work well with other plugins that expect to
  wrap or gain control of the test-running process. Examples from nose's 
  builtin plugins include coverage and profiling: a test run using
  both multiprocess and either of those is likely to fail in some
  confusing and spectacular way.

* Python 2.6 warning

  This is unlikely to impact you unless you are writing tests for nose itself,
  but be aware that under python 2.6, the multiprocess plugin is not
  re-entrant. For example, when running nose with the plugin active, you can't
  use subprocess to launch another copy of nose that also uses the
  multiprocess plugin. This is why this test is skipped under python 2.6 when
  run with the ``--processes`` switch.
