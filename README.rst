.. image:: https://img.shields.io/pypi/v/splinter.svg
    :target: https://pypi.org/project/splinter
    :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/splinter.svg
    :alt: PyPI - Python Version
    :target: https://github.com/cobrateam/splinter

.. image:: https://img.shields.io/github/license/cobrateam/splinter.svg
   :alt: GitHub
   :target: https://github.com/cobrateam/splinter/blob/master/LICENSE

.. image:: https://github.com/cobrateam/splinter/workflows/CI/badge.svg
   :target: https://github.com/cobrateam/splinter/actions/workflows/main.yml
   :alt: Build status

+++++++++++++++++++++++++++++++++++++++++++++++++++
splinter - python tool for testing web applications
+++++++++++++++++++++++++++++++++++++++++++++++++++

splinter is an open source tool for testing web applications using Python.
It lets you automate browser actions, such as visiting URLs and interacting with their items.

Sample code
-----------

.. code:: python

   from splinter import Browser

   browser = Browser()
   browser.visit('http://google.com')
   browser.fill('q', 'splinter - python acceptance testing for web applications')
   browser.find_by_name('btnK').click()

   if browser.is_text_present('splinter.readthedocs.io'):
       print("Yes, the official website was found!")
   else:
       print("No, it wasn't found... We need to improve our SEO techniques")

   browser.quit()

**Note:** if you don't provide any driver argument to the ``Browser`` function, ``firefox`` will be used (`Browser function documentation <https://splinter.readthedocs.io/en/latest/api/driver-and-element-api.html>`_).

`Changelog <https://splinter.readthedocs.io/en/latest/news.html>`_

First steps
===========

* `Installation <https://splinter.readthedocs.io/en/latest/install.html>`_

* `Quick tutorial <https://splinter.readthedocs.io/en/latest/tutorial.html>`_

Splinter open source project
============================

* `Community <https://splinter.readthedocs.io/en/latest/community.html>`_

* `Contribute <https://splinter.readthedocs.io/en/latest/contribute.html>`_

Documentation
=============

* `Splinter documentation <https://splinter.readthedocs.io>`_

Pytest Plugins
==============

* `pytest-splinter <http://pytest-splinter.readthedocs.io>`_, Splinter plugin for the `py.test <http://docs.pytest.org>`_ runner.

Page Objects
============

Support for page objects is available through the following package:

* `Stere <https://stere.readthedocs.io/>`_

Deprecated projects:
++++++++++++++++++++

* `PyPOM <http://pypom.readthedocs.io/>`_, A base page object model for use with Selenium or Splinter functional tests.

* `pypom_form <http://pypom-form.readthedocs.io>`_, A PyPOM based package that provides declarative schema based form interaction for page object models compatible with Splinter.

Other Projects Using Splinter
=============================

* `salad <https://github.com/salad/salad>`_, a nice mix of great BDD ingredients (splinter + `lettuce <http://lettuce.it>`_ integration)

* `behave-django <https://github.com/behave/behave-django>`_, BDD testing in Django using `Behave <https://github.com/behave/behave/>`_. Works well with splinter.


Presentations & Tutorials
=========================
* `Django Full Stack Testing and BDD with Lettuce and Splinter <https://www.cilliano.com/2011/02/07/django-bdd-with-lettuce-and-splinter.html>`_
