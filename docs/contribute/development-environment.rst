.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Find how to contribute to splinter.
    :keywords: splinter, python, contribution, open source, testing, web application

+++++++++++++++++++++++
Development Environment
+++++++++++++++++++++++

Setup
=====

Splinter is written in Python 3. It targets active Python versions and generally drops support
for versions as they hit end of life status. For platform support,
we target Linux, MacOS, and Windows.

Installing Python on your machine is out of scope for this documentation.

We use `virtual environments <https://docs.python.org/3/library/venv.html>`_ extensively
and manage them using `tox <https://tox.wiki/en/latest/>`_.

Generally, tox should be installed with pip:

.. code-block:: bash

  pip install tox

See tox's documentation if you need to use another method.


tox can then be run from the project root:

.. code-block:: bash

  cd /path/to/source_code
  # Lists the possible environments to use with `tox -e`
  tox l


Linting
=======

Splinter enforces code standards using various linting tools. They can be run from tox:

.. code-block:: bash

  tox -e lint


Testing
=======

The following tox environments each run a subset of the test suite:

  - tests_splinter
  - tests_lxml_drivers
  - tests_selenium
  - tests_selenium_remote
  - tests_selenium_edge
  - tests_selenium_safari

Run
---

Running any suite is as simple as passing the environment name to tox:

.. code-block:: bash

  tox -e tests_selenium


Documentation
=============

Our documentation is written using `Sphinx <https://www.sphinx-doc.org/>`_,
which uses the `RST <http://docutils.sourceforge.net/rst.html>`_ format.

For the documentation's visual theme, we use the `Sphinx-Immaterial Theme <https://jbms.github.io/sphinx-immaterial/>`_.


Build
-----

The `build_docs` environment is a wrapper around Sphinx's Makefile.
Arguments will be passed to the Makefile. Thus, to build the docs in HTML format:

.. code-block:: bash

  tox -e build_docs -- html


The documentation will then be built inside the `docs/_build/html` directory:

.. code-block:: bash

  open docs/_build/html/index.html
