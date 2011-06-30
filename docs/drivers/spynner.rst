.. meta::
    :description: How to use splinter with webkit via spynner for tests on web applications
    :keywords: splinter, python, tutorial, how to install, installation, spynner, webkit

++++++++++++++++
Spynner (WebKit)
++++++++++++++++

 **Note:** Spynner uses WebKit. In order to get it working, you need to :doc:`install PyQt4 </drivers/installing_pyqt>`.

 Spynner is a powerful headless browsing tool for Python, you can easily install it via pip:

 .. highlight:: bash

 ::

    $ [sudo] pip install spynner

Using Spynner driver
--------------------

To use the Spynner driver, all you need to do is pass the string ``webkit.spynner`` when you create
the ``Browser`` instance:

.. highlight:: python

::

    from splinter.browser import Browser
    browser = Browser('webkit.spynner')

**Note:** if you don't provide any driver to ``Browser`` function, ``webdriver.firefox`` will be used.
