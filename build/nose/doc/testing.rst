Testing with nose
=================

Writing tests is easier
-----------------------

nose collects tests from :class:`unittest.TestCase` subclasses, of course. But
you can also write simple test functions, as well as test classes that are
*not* subclasses of :class:`unittest.TestCase`. nose also supplies a number of
helpful functions for writing timed tests, testing for exceptions, and other
common use cases. See :doc:`writing_tests` and :doc:`testing_tools` for more.

Running tests is easier
-----------------------

nose collects tests automatically, as long as you follow some simple
guidelines for organizing your library and test code. There's no need
to manually collect test cases into test suites. Running tests is
responsive, since nose begins running tests as soon as the first test
module is loaded. See :doc:`finding_tests` for more.

Setting up your test environment is easier
------------------------------------------

nose supports fixtures at the package, module, class, and test case
level, so expensive initialization can be done as infrequently as
possible. See :ref:`fixtures` for more.

Doing what you want to do is easier
-----------------------------------

nose comes with a number of :doc:`builtin plugins <plugins/builtin>` to help
you with output capture, error introspection, code coverage, doctests, and
more. It also comes with plugin hooks for loading, running, watching and
reporting on tests and test runs. If you don't like the default collection
scheme, or it doesn't suit the layout of your project, or you need reports in
a format different from the unittest standard, or you need to collect some
additional information about tests (like code coverage or profiling data), you
can write a plugin to make nose do what you want. See the section on
:doc:`plugins/writing` for more.  There are also many 
`third-party nose plugins <http://nose-plugins.jottit.com/>`_ available.

Details
-------

.. toctree ::
   :maxdepth: 2

   usage
   writing_tests
   finding_tests
   testing_tools
   plugins/builtin
   plugins/other
   setuptools_integration
