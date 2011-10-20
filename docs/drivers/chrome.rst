.. meta::
    :description: How to use splinter with Chrome webdriver
    :keywords: splinter, python, tutorial, how to install, installation, chrome, selenium

++++++++++++++++
Chrome WebDriver
++++++++++++++++

Chrome WebDriver is provided by Selenium 2.0. To use it, you need to install Selenium 2.0 via pip:

.. highlight:: bash

::

    $ [sudo] pip install selenium

It's important to note that you also need to have Google Chrome installed in your machine.

Setting up Chrome WebDriver
---------------------------

In order to use `Google Chrome <http://google.com/chrome>`_ with Splinter, since we're using Selenium 2.0 RC2,
you need to setup Chrome webdriver properly. All you need to do is `download <http://code.google.com/p/selenium/downloads/list>`_
a prebuilt distribution of ChromeDriver server and put it in your ``PATH``.

Windows
-------

    **Note:** We don't provide official support for Windows, but you can try it by yourself.

All you need to do is go to `download page on Selenium project <http://code.google.com/p/selenium/downloads/list>`_ and choose
"ChromeDriver server for win32". Your browser will download a zip file, extract it and add the ``.exe`` file to your PATH.

If you don't know how to add an executable to the PATH on Windows, check these link out:

* `Environment variables <http://msdn.microsoft.com/en-us/library/ms682653.aspx>`_
* `How to manage environment variables in Windows XP <http://support.microsoft.com/kb/310519>`_

Linux and Mac OS X
------------------

Go to the `download page on Selenium project <http://code.google.com/p/selenium/downloads/list>`_ and choose
the properly version for you Linux (32 or 64 bits) or Mac OS ("ChromeDriver server for Mac OSX"). Then extract the
downloaded file in a directory in the ``PATH`` (e.g. ``/usr/bin``). You can also extract it to any directory
and add that directory to the ``PATH``:

.. highlight:: bash

::

    $ cd $HOME/Downloads
    $ wget http://selenium.googlecode.com/files/chromedriver_mac_13.0.775.0.zip
    $ unzip chromedriver_mac_13.0.775.zip
    $ mkdir -p $HOME/bin
    $ mv chromedriver $HOME/bin
    $ echo "export PATH=$PATH:$HOME/bin" >> $HOME/.bash_profile

Using Chrome WebDriver
----------------------

To use the Chrome driver, all you need to do is pass the string ``webdriver.chrome`` when you create
the ``Browser`` instance:

.. highlight:: python

::

    from splinter.browser import Browser
    browser = Browser('firefox.chrome')

**Note:** if you don't provide any driver to ``Browser`` function, ``webdriver.firefox`` will be used.
