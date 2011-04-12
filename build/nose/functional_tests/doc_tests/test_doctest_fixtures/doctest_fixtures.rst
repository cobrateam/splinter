Doctest Fixtures
----------------

Doctest files, like other tests, can be made more efficient or meaningful or
at least easier to write by judicious use of fixtures. nose supports limited
fixtures for use with doctest files. 

Module-level fixtures
=====================

Fixtures for a doctest file may define any or all of the following methods for
module-level setup:

* setup
* setup_module
* setupModule
* setUpModule

Each module-level setup function may optionally take a single argument, the
fixtures module itself.

Example::

  def setup_module(module):
      module.called[:] = []

Similarly, module-level teardown methods are available, which also optionally
take the fixtures module as an argument:
      
* teardown
* teardown_module
* teardownModule
* tearDownModule

Example::

  def teardown_module(module):
      module.called[:] = []
      module.done = True

Module-level setup executes **before any tests are loaded** from the doctest
file. This is the right place to raise :class:`nose.plugins.skip.SkipTest`,
for example.
      
Test-level fixtures
===================

In addition to module-level fixtures, *test*-level fixtures are
supported. Keep in mind that in the doctest lexicon, the *test* is the *entire
doctest file* -- not each individual example within the file. So, like the
module-level fixtures, test-level fixtures execute *once per file*. The
differences are that:

- test-level fixtures execute **after** tests have been loaded, but **before**
  any tests have executed.
- test-level fixtures receive the doctest :class:`doctest.DocFileCase` loaded
  from the file as their one *required* argument.
      
**setup_test(test)** is called before the test is run.

Example::

  def setup_test(test):
      called.append(test)
      test.globs['count'] = len(called)
  setup_test.__test__ = False
      
**teardown_test(test)** is alled after the test, unless setup raised an
uncaught exception. The argument is the :class:`doctest.DocFileCase` object,
*not* a unittest.TestCase.

Example::

  def teardown_test(test):
      pass
  teardown_test.__test__ = False
  
Bottom line: setup_test, teardown_test have access to the *doctest test*,
while setup, setup_module, etc have access to the *fixture*
module. setup_module runs before tests are loaded, setup_test after.

.. note ::

   As in the examples, it's a good idea to tag your setup_test/teardown_test
   functions with ``__test__ = False`` to avoid them being collected as tests.

Lastly, the fixtures for a doctest file may supply a **globs(globs)**
function. The dict returned by this function will be passed to the doctest
runner as the globals available to the test. You can use this, for example, to
easily inject a module's globals into a doctest that has been moved from the
module to a separate file. 

Example
=======

This doctest has some simple fixtures:

.. include :: doctest_fixtures_fixtures.py
   :literal:

The ``globs`` defined in the fixtures make the variable ``something``
available in all examples.
   
    >>> something
    'Something?'

The ``count`` variable is injected by the test-level fixture.
    
    >>> count
    1

.. warning ::

  This whole file is one doctest test. setup_test doesn't do what you think!
  It exists to give you access to the test case and examples, but it runs
  *once*, before all of them, not before each.

    >>> count
    1

  Thus, ``count`` stays 1 throughout the test, no matter how many examples it
  includes.