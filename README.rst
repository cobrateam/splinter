.. image:: https://secure.travis-ci.org/cobrateam/splinter.svg?branch=master
   :target: http://travis-ci.org/cobrateam/splinter

++++++++++++++++++++++++++++++++++++++++++++++++
splinter - python tool for testing web applications
++++++++++++++++++++++++++++++++++++++++++++++++

splinter is an open source tool for testing web applications using Python.
It lets you automate browser actions, such as visiting URLs and interacting with their items.

Sample code
-----------

.. highlight:: python

::
   
   from splinter import Browser

   browser = Browser()
   browser.visit('http://google.com')
   browser.fill('q', 'splinter - python acceptance testing for web applications')
   browser.find_by_name('btnG').click()

   if browser.is_text_present('splinter.readthedocs.io'):
       print "Yes, the official website was found!"
   else:
       print "No, it wasn't found... We need to improve our SEO techniques"

   browser.quit()
`What's new in splinter? <https://splinter.readthedocs.io/en/latest/news.html>`_

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

External links
==============

* `Django Full Stack Testing and BDD with Lettuce and Splinter <http://cilliano.com/blog/2011/02/07/django-bdd-with-lettuce-and-splinter/>`_

* `Splinter: Python tool for acceptance tests on web applications <http://www.franciscosouza.com/2011/05/splinter-python-tool-for-acceptance-tests-on-web-applications/>`_

* `Testes de aceitação com Lettuce e Splinter (pt-br) <http://www.slideshare.net/franciscosouza/testes-de-aceitao-com-lettuce-e-splinter?from=ss_embed>`_

* `salad <https://github.com/salad/salad>`_, a nice mix of great BDD ingredients (splinter + `lettuce <http://lettuce.it>`_ integration)

* `behave-django <https://github.com/mixxorz/behave-django>`_, BDD testing in Django using `Behave <http://pythonhosted.org/behave/>`_. Works well with splinter.

* `pytest-splinter <http://pytest-splinter.readthedocs.io>`_, Splinter plugin for the `py.test <http://docs.pytest.org>`_ runner.

* `PyPOM <http://pypom.readthedocs.io/>`_, PyPOM, or Python Page Object Model, is a Python library that provides a base page object model for use with Selenium or Splinter functional tests.

* `pypom_form <http://pypom-form.readthedocs.io>`_, is a PyPOM based package that provides declarative schema based form interaction for page object models compatible with Splinter.
