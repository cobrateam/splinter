.. meta::
    :description: How to use splinter with Firefox webdriver
    :keywords: splinter, python, tutorial, how to install, installation, firefox, selenium

+++++++++++++++++
Firefox WebDriver
+++++++++++++++++

Firefox WebDriver is provided by Selenium 2.0. To use it, you need to install Selenium 2.0 via pip:

.. highlight:: bash

::

    $ [sudo] pip install selenium

It's important to note that you also need to have `Firefox <http://firefox.com>`_ installed in your machine.
Once you have it installed, there is nothing you have to do, just use it :)

Using Firefox WebDriver
-----------------------

To use the Firefox driver, all you need to do is pass the string ``webdriver.firefox`` when you create
the ``Browser`` instance:

.. highlight:: python

::

    from splinter.browser import Browser
    browser = Browser('firefox.webdriver')

**Note:** if you don't provide any driver to ``Browser`` function, ``webdriver.firefox`` will be used.
