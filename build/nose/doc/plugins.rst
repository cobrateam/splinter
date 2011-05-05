Extending and customizing nose with plugins
===========================================

nose has plugin hooks for loading, running, watching and reporting on tests and
test runs. If you don't like the default collection scheme, or it doesn't suit
the layout of your project, or you need reports in a format different from the
unittest standard, or you need to collect some additional information about
tests (like code coverage or profiling data), you can write a plugin to do so.
See the section on `writing plugins`_ for more. 

nose also comes with a number of built-in plugins, such as:

* Output capture
  
  Unless called with the ``-s`` (``--nocapture``) switch, nose will capture
  stdout during each test run, and print the captured output only for tests
  that fail or have errors. The captured output is printed immediately
  following the error or failure output for the test. (Note that output in
  teardown methods is captured, but can't be output with failing tests, because
  teardown has not yet run at the time of the failure.)

* Assert introspection

  When run with the ``-d`` (``--detailed-errors``) switch, nose will try to
  output additional information about the assert expression that failed with
  each failing test. Currently, this means that names in the assert expression
  will be expanded into any values found for them in the locals or globals in
  the frame in which the expression executed.
  
  In other words, if you have a test like::
  
    def test_integers():
        a = 2
        assert a == 4, "assert 2 is 4"
    
  You will get output like::
    
      File "/path/to/file.py", line XX, in test_integers:
           assert a == 4, "assert 2 is 4"
      AssertionError: assert 2 is 4
        >>  assert 2 == 4, "assert 2 is 4"
    
  Please note that dotted names are not expanded, and callables are not called
  in the expansion.

See below for the rest of the built-in plugins.

Using Builtin plugins
---------------------

See :doc:`plugins/builtin`

Writing plugins
---------------

.. toctree ::
   :maxdepth: 2
   
   plugins/writing
   plugins/interface
   plugins/errorclasses
   plugins/documenting
   
Testing plugins
---------------

.. toctree ::
   :maxdepth: 2
   
   plugins/testing