.. Copyright © 2018 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Setting up your development environment for Splinter.
    :keywords: splinter, open source, python, contribute, development environment

+++++++++++++++++++++++++++++++++++++++++++++++
Setting up your splinter development environment
+++++++++++++++++++++++++++++++++++++++++++++++

Setting up a splinter development environment is a really easy task. Once you have some
basic development tools on your machine, you can set up the entire environment with just one command.

Basic development tools
=======================

Let's deal with those tools first.

macOS
------

If you're a macOS user, you just need to install Xcode, which can be downloaded
from Mac App Store (on Snow Leopard or later) or from
`Apple website <https://developer.apple.com/download/>`_.

Linux
-----

If you are running a Linux distribution, you need to install some basic development libraries
and headers. For example, on Ubuntu, you can easily install all of them using ``apt-get``:

.. highlight:: bash

::

    $ [sudo] apt-get install build-essential python-dev libxml2-dev libxslt1-dev

PIP and virtualenv
------------------

Make sure you have pip installed. We manage all splinter development dependencies with
`PIP <https://pip.pypa.io/en/stable/>`_, so you should use it too.

And please, for the sake of a nice development environment, use `virtualenv <https://pypi.org/project/virtualenv/>`_.
If you aren't using it yet, start now. :)

Dependencies
------------

Once you have all development libraries installed for your OS, just install all splinter development dependencies with
``make``:

.. highlight:: bash

::

    $ [sudo] make dependencies

**Note:** You will need ``sudo`` only if you aren't using virtualenv (which means you're a really bad guy - *no donuts for you*).

Also make sure you have properly configured your :doc:`Chrome driver </drivers/chrome>`.
