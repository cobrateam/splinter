.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Find how to contribute with splinter.
    :keywords: splinter, python, contribution, open source, testing, web application, atdd

++++++++++
Contribute
++++++++++

* Source hosted at `GitHub <http://github.com/cobrateam/splinter>`_
* Report issues on `GitHub Issues <http://github.com/cobrateam/splinter/issues>`_

Pull requests are very welcome! Make sure your patches are well tested and documented :)

If you want to add any new driver, check out our :doc:`docs for creating new splinter drivers </contribute/writing-new-drivers>`.

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

Splinter documentation is written using `Sphinx 
<http://sphinx.pocoo.org/>`_, which uses `RST 
<http://docutils.sourceforge.net/rst.html>`_. We use the `Read the Docs Sphinx Theme <https://sphinx-rtd-theme.readthedocs.io/en/latest/index.html>`_. Check these tools' docs to learn how to write docs for Splinter.

building docs
=============

In order to build the HTML docs, just navigate to the project folder
(the main folder, not the ``docs`` folder) and run the following on the terminal:

.. highlight:: bash

::

    $ make doc

The requirements for building the docs are specified in
``doc-requirements.txt`` in the project folder.
