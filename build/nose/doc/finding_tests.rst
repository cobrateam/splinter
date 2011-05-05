Finding and running tests
-------------------------

nose, by default, follows a few simple rules for test discovery.

* If it looks like a test, it's a test. Names of directories, modules,
  classes and functions are compared against the testMatch regular
  expression, and those that match are considered tests. Any class that is a
  `unittest.TestCase` subclass is also collected, so long as it is inside of a
  module that looks like a test.
   
* Directories that don't look like tests and aren't packages are not
  inspected.

* Packages are always inspected, but they are only collected if they look
  like tests. This means that you can include your tests inside of your
  packages (somepackage/tests) and nose will collect the tests without
  running package code inappropriately.

* When a project appears to have library and test code organized into
  separate directories, library directories are examined first.

* When nose imports a module, it adds that module's directory to sys.path;
  when the module is inside of a package, like package.module, it will be
  loaded as package.module and the directory of *package* will be added to
  sys.path.

* If an object defines a __test__ attribute that does not evaluate to
  True, that object will not be collected, nor will any objects it
  contains.

Be aware that plugins and command line options can change any of those rules.