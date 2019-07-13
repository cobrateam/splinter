.. Copyright 2014 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: How to use splinter with Flask.
    :keywords: splinter, python, tutorial, how to install, installation, Flask

++++++++++++
Flask client
++++++++++++

.. module:: splinter.driver.flaskclient

To use the ``flask`` driver, you need to install `Flask <https://pypi.python.org/pypi/Flask>`_, 
`lxml <https://pypi.python.org/pypi/lxml>`_ and `cssselect <http://pypi.python.org/pypi/cssselect>`_. 
You can install all of them in one step by running:

.. highlight:: bash

::

    $ pip install splinter[flask]

Using Flask client
-------------------

To use the ``flask`` driver, you'll need to pass the string ``flask`` and an app instances via the
``app`` keyword argument when you create the ``Browser`` instance:

.. highlight:: python

::

    from splinter import Browser
    browser = Browser('flask', app=app)

**Note:** if you don't provide any driver to ``Browser`` function, ``firefox`` will be used.

When visiting pages with the Flask client, you only need to provide a path rather than a full URL.
For example:

.. highlight:: python

::

    browser.visit('/my-path')

API docs
--------

.. autoclass:: FlaskClient
   :members:
   :inherited-members:
