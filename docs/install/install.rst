.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Install guide for splinter
    :keywords: splinter, python, tutorial, how to install, installation

++++++++++++++++
Install Splinter
++++++++++++++++

Basic Requirements
==================

Splinter officially supports Python versions 3.8 and up.

pip
===

To install the latest release, run the following command in the terminal:

.. code-block:: bash

	   pip install splinter


Install With Driver Dependencies
--------------------------------

pip can be given extra arguments to automatically install driver dependencies.

The :ref:`Install Drivers <install-drivers>` section of the documentation has more information for each driver.

.. highlight:: bash

::

  $ pip install splinter[selenium]


From Source Code
================

Splinter's source code is hosted on `GitHub <https://github.com/cobrateam/splinter>`_.
You can clone the repository using `git <https://git-scm.com/>`_:

.. highlight:: bash

::

    $ git clone git://github.com/cobrateam/splinter.git


Once you have a copy of the source code, you can manually install the package:

.. highlight:: bash

::

    $ cd splinter
    $ pip install .
