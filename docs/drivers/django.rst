.. Copyright 2014 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: How to use splinter with django.
    :keywords: splinter, python, tutorial, how to install, installation, django

++++++
Django
++++++

.. module:: splinter.driver.djangoclient

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
