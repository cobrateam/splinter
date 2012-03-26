.. meta::
    :description: Find how to write new drivers for splinter.
    :keywords: splinter, python, contribution, open source, testing, web application, atdd, drivers

++++++++++++++++++++++++++++
writing new splinter drivers
++++++++++++++++++++++++++++

The process of creating a new splinter browser is really simple: you just need to implement a
TestCase (extending ``tests.base. BaseBrowserTests``) and make all tests green.

Here is an example: imagine you're creating the ``Columbia`` driver, you would add the ``test_columbia.py``
file containing some code like this:

.. highlight:: python

::

    from splinter import Browser
    from tests.base import BaseBrowserTests

    class ColumbiaTest(BaseBrowserTests):

        @classmethod
        def setUpClass(cls):
            cls.browser = Browser('columbia')

        # ...

Now, to make the test green, you need to implement methods provided by the
`DriverAPI <https://github.com/cobrateam/splinter/blob/master/splinter/driver/__init__.py#L10>`_ and
the `ElementAPI <https://github.com/cobrateam/splinter/blob/master/splinter/driver/__init__.py#L172>`_.

Use ``make test`` to run the tests:

.. highlight:: bash

::

    $ make test which=tests/test_columbia.py
