.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Setting up your development environment for Splinter.
    :keywords: splinter, open source, python, contribute, development environment

+++++++++++++++++++++++++++++++++++++++++++++++
Setting up you splinter development environment
+++++++++++++++++++++++++++++++++++++++++++++++

Setting up a splinter development environment is a really easy task, you need to make sure you have some
basic development tools in your machine, you can setup the entire environment with just one command.

Basic development tools
=======================

Let's deal with those tools first.

Mac OS
------

If you're a Mac OS user, you just need to install XCode, which can be downloaded
from Mac App Store (on Mac OS X Lion) or from
`Apple website <http://connect.apple.com/cgi-bin/WebObjects/MemberSite.woa/wa/getSoftware?bundleID=20792>`_.

Linux
-----

If you are running a Linux in your computer, you need to install some basic development libraries
and headers. On Ubuntu, you can easily install all of them using ``apt-get``:

.. highlight:: bash

::

    $ [sudo] apt-get install build-essential python-dev libxml2-dev libxslt1-dev

PIP and virtualenv
------------------

Make sure you have pip installed. We manage all splinter development dependencies with
`PIP <http://pip-installer.org>`_, so you should use it for too.

And please, for the sake of a nice development environment, use `virtualenv <http://virtualenv.org>`_.
If you aren't using it yet, start now. :)

Dependencies
------------

Once you had all development libraries installed for you OS, just install all splinter development dependencies with
``make``:

.. highlight:: bash

::

    $ [sudo] make dependencies

**Note:** You will need ``sudo`` only if you aren't using virtualenv (which means you're a really bad guy - *no donuts for you*).

Also make sure you have properly configured you :doc:`Chrome driver </drivers/chrome>`.
