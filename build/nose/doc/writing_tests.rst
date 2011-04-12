Writing tests
-------------

As with py.test_, nose tests need not be subclasses of
:class:`unittest.TestCase`. Any function or class that matches the configured
testMatch regular expression (``(?:^|[\\b_\\.-])[Tt]est)`` by default -- that
is, has test or Test at a word boundary or following a - or _) and lives in a
module that also matches that expression will be run as a test. For the sake
of compatibility with legacy unittest test cases, nose will also load tests
from :class:`unittest.TestCase` subclasses just like unittest does. Like
py.test, nose runs functional tests in the order in which they appear in the
module file. TestCase-derived tests and other test classes are run in
alphabetical order.

.. _py.test: http://codespeak.net/py/current/doc/test.html

.. _fixtures:

Fixtures
========

nose supports fixtures (setup and teardown methods) at the package,
module, class, and test level. As with py.test or unittest fixtures,
setup always runs before any test (or collection of tests for test
packages and modules); teardown runs if setup has completed
successfully, regardless of the status of the test run. For more detail
on fixtures at each level, see below.

Test packages
=============

nose allows tests to be grouped into test packages. This allows
package-level setup; for instance, if you need to create a test database
or other data fixture for your tests, you may create it in package setup
and remove it in package teardown once per test run, rather than having to
create and tear it down once per test module or test case.

To create package-level setup and teardown methods, define setup and/or
teardown functions in the ``__init__.py`` of a test package. Setup methods may
be named `setup`, `setup_package`, `setUp`, or `setUpPackage`; teardown may
be named `teardown`, `teardown_package`, `tearDown` or `tearDownPackage`.
Execution of tests in a test package begins as soon as the first test
module is loaded from the test package.

Test modules
============

A test module is a python module that matches the testMatch regular
expression. Test modules offer module-level setup and teardown; define the
method `setup`, `setup_module`, `setUp` or `setUpModule` for setup,
`teardown`, `teardown_module`, or `tearDownModule` for teardown. Execution
of tests in a test module begins after all tests are collected.

Test classes
============

A test class is a class defined in a test module that matches testMatch or is
a subclass of :class:`unittest.TestCase`. All test classes are run the same
way: Methods in the class that match testMatch are discovered, and a test
case is constructed to run each method with a fresh instance of the test
class. Like :class:`unittest.TestCase` subclasses, other test classes can
define setUp and tearDown methods that will be run before and after each test
method. Test classes that do not descend from `unittest.TestCase` may also
include generator methods and class-level fixtures. Class-level setup fixtures
may be named `setup_class`, `setupClass`, `setUpClass`, `setupAll` or 
`setUpAll`; teardown fixtures may be named `teardown_class`, `teardownClass`, 
`tearDownClass`, `teardownAll` or `tearDownAll`. Class-level setup and teardown
fixtures must be class methods.

Test functions
==============

Any function in a test module that matches testMatch will be wrapped in a
`FunctionTestCase` and run as a test. The simplest possible failing test is
therefore::

  def test():
      assert False

And the simplest passing test::

  def test():
      pass

Test functions may define setup and/or teardown attributes, which will be
run before and after the test function, respectively. A convenient way to
do this, especially when several test functions in the same module need
the same setup, is to use the provided `with_setup` decorator::

  def setup_func():
      "set up test fixtures"

  def teardown_func():
      "tear down test fixtures"

  @with_setup(setup_func, teardown_func)
  def test():
      "test ..."

For python 2.3 or earlier, add the attributes by calling the decorator
function like so::

  def test():
      "test ... "
  test = with_setup(setup_func, teardown_func)(test)

or by direct assignment::

  test.setup = setup_func
  test.teardown = teardown_func
  
Please note that `with_setup` is useful *only* for test functions, not
for test methods in `unittest.TestCase` subclasses or other test
classes. For those cases, define `setUp` and `tearDown` methods in the
class.
  
Test generators
===============

nose supports test functions and methods that are generators. A simple
example from nose's selftest suite is probably the best explanation::

  def test_evens():
      for i in range(0, 5):
          yield check_even, i, i*3

  def check_even(n, nn):
      assert n % 2 == 0 or nn % 2 == 0

This will result in four tests. nose will iterate the generator, creating a
function test case wrapper for each tuple it yields. As in the example, test
generators must yield tuples, the first element of which must be a callable
and the remaining elements the arguments to be passed to the callable.

By default, the test name output for a generated test in verbose mode
will be the name of the generator function or method, followed by the
args passed to the yielded callable. If you want to show a different test
name, set the ``description`` attribute of the yielded callable.

Setup and teardown functions may be used with test generators. However, please
note that setup and teardown attributes attached to the *generator function*
will execute only once. To *execute fixtures for each yielded test*, attach
the setup and teardown attributes to the function that is yielded, or yield a
callable object instance with setup and teardown attributes.

For example::

  @with_setup(setup_func, teardown_func)
  def test_generator():
      # ...
      yield func, arg, arg # ...

Here, the setup and teardown functions will be executed *once*. Compare to::

  def test_generator():
      # ...
      yield func, arg, arg # ...

  @with_setup(setup_func, teardown_func)
  def func(arg):
      assert something_about(arg)

In the latter case the setup and teardown functions will execute once for each
yielded test.

For generator methods, the setUp and tearDown methods of the class (if any)
will be run before and after each generated test case. The setUp and tearDown
methods *do not* run before the generator method itself, as this would cause
setUp to run twice before the first test without an intervening tearDown.

Please note that method generators *are not* supported in `unittest.TestCase`
subclasses.