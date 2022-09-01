.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Find how to contribute to splinter.
    :keywords: splinter, python, contribution, open source, testing, web application

++++++++++++
Contributing
++++++++++++

The Source Code is hosted on `GitHub <http://github.com/cobrateam/splinter>`_

For small fixes, opening a new Pull Request in the project's repo is fine.

For larger issues or new features, please open an `issue <https://github.com/cobrateam/splinter/issues>`_ first.

If you want to add a new driver, check out our :doc:`docs for creating new splinter drivers </contribute/writing-new-drivers>`.

Before opening a new Pull Request, please ensure the linter and at least platform agnostic tests are passing on your branch.

Requirements
============

Tests should be run using `tox <https://tox.wiki/en/latest/>`_

Install tox from the command line:

.. highlight:: bash

::

  pip install tox


Linter
======

Splinter enforces code standards using various linting tools. They can be run from tox:

.. highlight:: bash

::

  tox -e lint


Tests
=====


Run
---

The tests are split into two groups: Platform agnostic and Windows-only.

To run the platform agnostic tests:

.. highlight:: bash

::

  tox -e tests -- tests/
  tox -e tests_selenium4 -- tests/


To run the windows tests:

.. highlight:: bash

::

  tox -e tests_windows -- tests/
  tox -e tests_windows_selenium4 -- tests/


You can also specify one or more test files to run:

.. highlight:: bash

::

  $ tox -e tests_windows_selenium4 -- tests/test_webdriver_firefox.py, tests/test_request_handler.py


Documentation
=============

Write
-----

Documentation is written using `Sphinx <http://sphinx.pocoo.org/>`_,
which uses `RST <http://docutils.sourceforge.net/rst.html>`_.

We use the `Read the Docs Sphinx Theme <https://sphinx-rtd-theme.readthedocs.io/en/latest/index.html>`_.


Build
-----

In order to build the HTML docs, navigate to the project folder
(the main folder, not the ``docs`` folder) and run the following command:

.. highlight:: bash

::

    $ make doc

The requirements for building the docs are specified in
``requirements/docs.txt`` in the project folder.
