.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: How to use splinter with Chrome webdriver
    :keywords: splinter, python, tutorial, how to install, installation, chrome, selenium

++++++++++++++++
Chrome WebDriver
++++++++++++++++

Chrome WebDriver is provided by Selenium2. To use it, you need to install Selenium2 via pip:

.. highlight:: bash

::

    $ [sudo] pip install selenium

It's important to note that you also need to have Google Chrome installed in your machine.

Setting up Chrome WebDriver
---------------------------

In order to use `Google Chrome <http://google.com/chrome>`_ with Splinter, since we're using Selenium 2.3.x,
you need to setup Chrome webdriver properly.


Mac OS X
--------

The recommended way is by using `Homebrew <http://mxcl.github.com/homebrew/>`_:

.. highlight:: bash

::

    $ brew install chromedriver


Linux
-----

Go to the `download page on Chromium project <https://code.google.com/p/chromedriver/downloads/list>`_ and choose
the properly version for you Linux (32 or 64 bits). Then extract the
downloaded file in a directory in the ``PATH`` (e.g. ``/usr/bin``). You can also extract it to any directory
and add that directory to the ``PATH``:


Linux 32bits
============

.. highlight:: bash

::

    $ cd $HOME/Downloads
    $ wget https://chromedriver.googlecode.com/files/chromedriver_linux32_20.0.1133.0.zip
    $ unzip chromedriver_linux32_20.0.1133.0.zip


Linux 64bits
============

.. highlight:: bash

::

    $ cd $HOME/Downloads
    $ wget https://chromedriver.googlecode.com/files/chromedriver_linux64_20.0.1133.0.zip
    $ unzip chromedriver_linux64_20.0.1133.0.zip


Linux (common steps for 32 and 64bits)
======================================

.. highlight:: bash

::

    $ mkdir -p $HOME/bin
    $ mv chromedriver $HOME/bin
    $ echo "export PATH=$PATH:$HOME/bin" >> $HOME/.bash_profile


Windows
-------

    **Note:** We don't provide official support for Windows, but you can try it by yourself.

All you need to do is go to `download page on Selenium project <https://code.google.com/p/chromedriver/downloads/list>`_ and choose
"ChromeDriver server for win". Your browser will download a zip file, extract it and add the ``.exe`` file to your PATH.

If you don't know how to add an executable to the PATH on Windows, check these link out:

* `Environment variables <http://msdn.microsoft.com/en-us/library/ms682653.aspx>`_
* `How to manage environment variables in Windows XP <http://support.microsoft.com/kb/310519>`_


Using Chrome WebDriver
----------------------

To use the Chrome driver, all you need to do is pass the string ``chrome`` when you create
the ``Browser`` instance:

.. highlight:: python

::

    from splinter import Browser
    browser = Browser('chrome')

**Note:** if you don't provide any driver to ``Browser`` function, ``firefox`` will be used.

**Note:** if you have trouble with ``$HOME/.bash_profile``, you can try ``$HOME/.bashrc``.

API docs
--------

.. autoclass:: splinter.driver.webdriver.chrome.WebDriver
   :members:
   :inherited-members:
