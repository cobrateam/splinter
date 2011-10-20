.. meta::
    :description: Find how to contribute with splinter.
    :keywords: splinter, python, contribution, open source, testing, web application, atdd

++++++++++
contribute
++++++++++

* Source hosted at `GitHub <http://github.com/cobrateam/splinter>`_
* Report issues on `GitHub Issues <http://github.com/cobrateam/splinter/issues>`_

Pull requests are very welcome! Make sure your patches are well tested and documented :)

running the tests
=================

If you are using a virtualenv, all you need is:

.. highlight:: bash

::

    $ make test

You can also specify one or more test files to run:

.. highlight:: bash

::

    $ make test which=tests/test_webdriver_firefox.py,tests/test_request_handler.py

You can pass which test files you want to run, separated by comma, to the ``which`` variable.

some conventions we like
========================

You can feel free to create and pull request new branches to Splinter project.
When adding support for new drivers, we usually work in a separated branch.


writing docs
============

Splinter documentation is written using `Sphinx <http://sphinx.pocoo.org/>`_, which uses `RST <http://docutils.sourceforge.net/rst.html>`_. Check these tools docs to learn how to write docs for Splinter.

building docs
=============

In order to build the HTML docs, just run on terminal:

.. highlight:: bash

::

    $ make doc
