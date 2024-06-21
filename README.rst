++++++++
splinter
++++++++

Splinter is a simple and consistent API for web application automation.

.. |pypi| image:: https://img.shields.io/pypi/v/splinter.svg
  :target: https://pypi.org/project/splinter
  :alt: PyPI

.. |pypi_version| image:: https://img.shields.io/pypi/pyversions/splinter.svg
  :alt: PyPI - Python Version
  :target: https://github.com/cobrateam/splinter

.. |license| image:: https://img.shields.io/github/license/cobrateam/splinter.svg
  :alt: License
  :target: https://github.com/cobrateam/splinter/blob/master/LICENSE

.. |build| image:: https://github.com/cobrateam/splinter/actions/workflows/main.yml/badge.svg
  :target: https://github.com/cobrateam/splinter/actions/workflows/main.yml
  :alt: Build status

|pypi| |pypi_version| |license| |build|

* `Documentation <https://splinter.readthedocs.io>`_

* `Changelog <https://splinter.readthedocs.io/en/latest/changelog.html>`_

Key features:

- Easy to learn: The API is designed to be intuitive and quick to pick up.
- Faster to code: Automate browser interactions quickly and reliably without fighting the tool.
- Powerful: Designed for real world use cases, it guards against common automation quirks.
- Flexible: Access to lower level tools is never hidden. Break out into raw Selenium at any time.
- Robust: Support is available for multiple automation drivers (Selenium, Django, Flask, ZopeTestBrowser).

Example
-------

.. code:: python

   from splinter import Browser


   browser = Browser('firefox')
   browser.visit('http://google.com')
   browser.find_by_name('q').fill('splinter - python acceptance testing for web applications')
   browser.find_by_name('btnK').click()

   if browser.is_text_present('splinter.readthedocs.io'):
       print("Yes, the official website was found!")
   else:
       print("No, it wasn't found... We need to improve our SEO techniques")

   browser.quit()


Getting Started
===============

* `Installation <https://splinter.readthedocs.io/en/latest/install/install.html>`_

* `Tutorial <https://splinter.readthedocs.io/en/latest/tutorial.html>`_


Pytest Plugins
==============

* `pytest-splinter <http://pytest-splinter.readthedocs.io>`_, Splinter plugin for the `py.test <http://docs.pytest.org>`_ runner.


Page Objects
============

Support for page objects is available through the following package:

* `Stere <https://stere.readthedocs.io/>`_
