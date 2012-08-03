.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Install guide for splinter
    :keywords: splinter, python, tutorial, how to install, installation

+++++++++++++
Install guide
+++++++++++++

Install Python
==============

In order to install Splinter, make sure Python is installed. Note: only Python between 2.5 - 2.7 are supported. Version 3.0 is not supported yet.

Download Python from http://www.python.org. If you’re using Linux or Mac OS X, it is probably already installed.

Install splinter
================

Basically, there are two ways to install Splinter:

Install a stable release
------------------------

If you're interested on an official and almost bug-free version, just run from the Terminal:


.. highlight:: bash

::

	$ [sudo] pip install splinter



Install under-development source-code
-------------------------------------

Otherwise, if you want Splinter's latest-and-greatest features and aren't afraid of running under development code, run:

.. highlight:: bash

::

    $ git clone git://github.com/cobrateam/splinter.git
    $ cd splinter
    $ [sudo] python setup.py install


**Notes:**

    * - make sure you have already :doc:`set up your development environment </contribute/setting-up-your-development-environment>`.
    * - in this second case, make sure `Git <http://git-scm.com/>`_  is installed.
    * - in order to use Chrome webdriver, you need to :doc:`setup Google Chrome properly </drivers/chrome>`.
