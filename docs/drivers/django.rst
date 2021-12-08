.. Copyright 2014 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: How to use splinter with django.
    :keywords: splinter, python, tutorial, how to install, installation, django

++++++
Django
++++++

Dependencies
------------

.. module:: splinter.driver.djangoclient

To use the ``django`` driver, the following must be installed:

`django <http://pypi.python.org/pypi/django>`_,
`lxml <https://pypi.python.org/pypi/lxml>`_,
`cssselect <http://pypi.python.org/pypi/cssselect>`_.

When splinter is installed via pip, the `django` extra argument can be provided.
This will automatically install Django.

.. code-block:: bash

    python -m pip install splinter[django]

Usage
-----

To use the ``django`` driver, all you need to do is pass the string ``django`` when you create
the ``Browser`` instance:

.. code-block:: python

    from splinter import Browser
    browser = Browser('django')

**Note:** if you don't provide any driver to ``Browser`` function, ``firefox`` will be used.

API docs
--------

.. autoclass:: splinter.driver.djangoclient.DjangoClient
   :members:
   :inherited-members:
   :exclude-members: execute_script, evaluate_script
