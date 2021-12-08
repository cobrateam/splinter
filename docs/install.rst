.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Install guide for splinter
    :keywords: splinter, python, tutorial, how to install, installation

++++++++++++++++++
Installation Guide
++++++++++++++++++

Basic Requirements
==================

Splinter officially supports Python versions 3.6+ for Selenium 3, Django, Flask, and zope.testbrowser.

For Selenium 4, Python versions 3.7+ are supported.

Latest version via pip
======================

To install the latest release, run the following command in the terminal:

.. code-block:: bash

	   python -m pip install splinter


Installing Driver Dependencies
------------------------------

pip can be given extra arguments to automatically install driver dependencies.

The `Drivers` section of the documentation has more information for each driver.

.. highlight:: bash

::

  $ python -m pip install splinter[django]


Source Code
===========

Splinter's source code is hosted on `GitHub <https://github.com/cobrateam/splinter>`_.
You can clone the repository using `git <https://git-scm.com/>`_:

.. highlight:: bash

::

    $ git clone git://github.com/cobrateam/splinter.git


Once you have a copy of the source code, you can manually install the package:

.. highlight:: bash

::

    $ cd splinter
    $ python setup.py install
