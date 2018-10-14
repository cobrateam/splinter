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

Chrome can also be used from a custom path. To do this pass the executable path as a dictionary to the `**kwargs` argument. The dictionary should be set up with `executable_path` as the key and the value set to the path to the executable file.

.. highlight:: python

::

    from splinter import Browser
    executable_path = {'executable_path':'</path/to/chrome>'}

    browser = Browser('chrome', **executable_path)

Setting up Chrome WebDriver
---------------------------

In order to use `Google Chrome <http://google.com/chrome>`_ with Splinter, since we're using Selenium 2.3.x,
you need to setup Chrome webdriver properly.


Mac OS X
--------

The recommended way is by using `Homebrew <http://mxcl.github.com/homebrew/>`_:

.. highlight:: bash

::

    $ brew cask install chromedriver


Linux
-----

Go to the `download page on the Chromium project
<https://sites.google.com/a/chromium.org/chromedriver/downloads>`_ and choose
the correct version for your Linux installation. Then extract the downloaded file in a
directory in the ``PATH`` (e.g. ``/usr/bin``). You can also extract it to any
directory and add that directory to the ``PATH``:

Linux 64bits
============

.. highlight:: bash

::

    $ cd $HOME/Downloads
    $ wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
    $ unzip chromedriver_linux64.zip

    $ mkdir -p $HOME/bin
    $ mv chromedriver $HOME/bin
    $ echo "export PATH=$PATH:$HOME/bin" >> $HOME/.bash_profile


Windows
-------

    **Note:** We don't provide official support for Windows, but you can try it by yourself.

All you need to do is go to `download page on Selenium project <https://sites.google.com/a/chromium.org/chromedriver/downloads>`_ and choose
"ChromeDriver server for win". Your browser will download a zip file, extract it and add the ``.exe`` file to your PATH.

If you don't know how to add an executable to the PATH on Windows, check these link out:

* `Environment variables <http://msdn.microsoft.com/en-us/library/ms682653.aspx>`_
* `How to manage environment variables in Windows XP <http://support.microsoft.com/kb/310519>`_
* `How to manage environment variables in Windows 8 & 10 <https://www.computerhope.com/issues/ch000549.htm>`_


Using Chrome WebDriver
----------------------

To use the Chrome driver, all you need to do is pass the string ``chrome`` when you create
the ``Browser`` instance:

.. highlight:: python

::

    from splinter import Browser
    browser = Browser('chrome')

**Note:** if you don't provide any driver to the ``Browser`` function, ``firefox`` will be used.

**Note:** if you have trouble with ``$HOME/.bash_profile``, you can try ``$HOME/.bashrc``.

Using headless option for Chrome
--------------------------------

Starting with Chrome 59, we can run Chrome as a headless browser.
Make sure you read `google developers updates <https://developers.google.com/web/updates/2017/05/nic59#headless>`_

.. highlight:: python

::

    from splinter import Browser
    browser = Browser('chrome', headless=True)

Using incognito option for Chrome
--------------------------------

We can run Chrome as a incognito browser.

.. highlight:: python

::

    from splinter import Browser
    browser = Browser('chrome', incognito=True)

Using emulation mode in Chrome
------------------------------

Chrome options can be passed to customize Chrome's behaviour; it is then possible to leverage the
experimental emulation mode.

.. highlight:: python

::

    from selenium import webdriver
    from splinter import Browser

    mobile_emulation = {"deviceName": "Google Nexus 5"}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation",
                                           mobile_emulation)
    browser = Browser('chrome', options=chrome_options)


refer to `chrome driver documentation <https://sites.google.com/a/chromium.org/chromedriver/mobile-emulation>`_


API docs
--------

.. autoclass:: splinter.driver.webdriver.chrome.WebDriver
   :members:
   :inherited-members:
