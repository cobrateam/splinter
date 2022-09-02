.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: How to use splinter with Chrome WebDriver
    :keywords: splinter, python, tutorial, how to install, installation, chrome, selenium

+++++++
Drivers
+++++++


Selenium-based Drivers
======================

To use ``chrome``, ``fireFox``, ``edge``, or ``remote``, the python bindings for Selenium 3 or Selenium 4 must be installed.

When splinter is installed via pip, the `selenium3` or `selenium4` extra argument can be provided.
This will automatically install the latest version of Selenium 3 or Selenium 4, respectively.


.. code-block:: bash

    python -m pip install splinter[selenium3]


.. code-block:: bash

    python -m pip install splinter[selenium4]


Microsoft Edge
==============

When using Selenium 3, ``edge`` also has the following dependency:

    - `msedge-selenium-tools <https://github.com/microsoft/edge-selenium-tools>`_

Using pip, it can be installed automatically as well:

.. code-block:: bash

    python -m pip install splinter[selenium3, edge]


Django
======

To use the ``django``, the following must be installed:

`django <http://pypi.python.org/pypi/django>`_,
`lxml <https://pypi.python.org/pypi/lxml>`_,
`cssselect <http://pypi.python.org/pypi/cssselect>`_.

When splinter is installed via pip, the `django` extra argument can be provided.
This will automatically install Django.

.. code-block:: bash

    python -m pip install splinter[django]


Flask
=====


To use the ``flask`` driver, the following must be installed:

`Flask <https://pypi.python.org/pypi/Flask>`_,
`lxml <https://pypi.python.org/pypi/lxml>`_,
`cssselect <http://pypi.python.org/pypi/cssselect>`_.

When splinter is installed via pip, the `flask` extra argument can be provided.
This will automatically install Flask.

.. code-block:: bash

    python -m pip install splinter[flask]


zope.testbrowser
================


To use the ``zope.testbrowser``, the following must be installed:

`zope.testbrowser <http://pypi.python.org/pypi/zope.testbrowser>`_,
`lxml <https://pypi.python.org/pypi/lxml>`_,
`cssselect <http://pypi.python.org/pypi/cssselect>`_.

When splinter is installed via pip, the `zope.testbrowser` extra argument can be provided.
This will automatically install Flask.

.. code-block:: bash

    python -m pip install splinter[zope.testbrowser]
