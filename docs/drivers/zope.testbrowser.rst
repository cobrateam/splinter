.. meta::
    :description: How to use splinter with zope.testbrowser
    :keywords: splinter, python, tutorial, how to install, installation, zope, testbrowser, zope.testbrowser

++++++++++++++++
zope.testbrowser
++++++++++++++++

In ``zope.testbrowser`` driver, we use `zope.testbrowser <http://pypi.python.org/pypi/zope.testbrowser>`_. You can install it via pip:

.. highlight:: bash

::

    $ [sudo] pip install zope.testbrowser

Using zope.testbrowser
----------------------

To use the ``zope.testbrowser`` driver, all you need to do is pass the string ``zope.testbrowser`` when you create
the ``Browser`` instance:

.. highlight:: python

::

    from splinter.browser import Browser
    browser = Browser('zope.testbrowser')

**Note:** if you don't provide any driver to ``Browser`` function, ``webdriver.firefox`` will be used.
