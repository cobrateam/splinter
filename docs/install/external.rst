+++++++++++++++++++++
Required Applications
+++++++++++++++++++++


Chrome
======


The following applications are required:

  - `Google Chrome <http://google.com/chrome>`_
  - `ChromeDriver <https://chromedriver.chromium.org/>`_

Chromedriver must also be available on your operating system's `PATH` environment variable.


Install
-------

Mac OS X
~~~~~~~~

The recommended way is by using `Homebrew <http://mxcl.github.com/homebrew/>`_:

.. code-block:: console

    brew install chromedriver


Linux
~~~~~

Go to the `download page on the Chromium project
<https://sites.google.com/chromium.org/driver/>`_ and choose
the correct version for your Linux installation. Then extract the downloaded file in a
directory in the ``PATH`` (e.g. ``/usr/bin``). You can also extract it to any
directory and add that directory to the ``PATH``:

Linux 64bits
~~~~~~~~~~~~

.. code-block:: console

    cd $HOME/Downloads
    wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip

    mkdir -p $HOME/bin
    mv chromedriver $HOME/bin
    echo "export PATH=$PATH:$HOME/bin" >> $HOME/.bash_profile


Windows
~~~~~~~

Go to the `download page on Selenium project <https://sites.google.com/a/chromium.org/chromedriver/downloads>`_ and choose
"ChromeDriver server for win". Your browser will download a zip file, extract it and add the ``.exe`` file to your PATH.

If you don't know how to add an executable to the PATH on Windows, check these link out:

* `Environment variables <http://msdn.microsoft.com/en-us/library/ms682653.aspx>`_
* `How to manage environment variables in Windows XP <http://support.microsoft.com/kb/310519>`_
* `How to manage environment variables in Windows 8 & 10 <https://www.computerhope.com/issues/ch000549.htm>`_


Firefox
=======


The following applications are required:

  - `Mozilla Firefox <http://firefox.com>`_
  - `Geckodriver <https://github.com/mozilla/geckodriver/releases>`_

Geckodriver must also be available on your operating system's `PATH` environment variable.


Install
-------

Mac OS X
~~~~~~~~

The recommended way is by using `Homebrew <http://mxcl.github.com/homebrew/>`_:

.. code-block:: console

    brew install geckodriver


Edge
====


The following applications are required:

  - `Microsoft Edge <https://www.microsoft.com/edge>`_
  - `Microsoft Edge Driver <https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/>`_

Microsoft Edge Driver must also be available on your operating system's `PATH` environment variable.


Install
-------

Mac OS X
~~~~~~~~

Modern versions of Edge (79+) are available for Mac OS X.
However, no versions of Edge Legacy are available.


Linux
~~~~~

Neither version of Edge is available for Linux, and thus Edge WebDriver
cannot be used on Linux systems.
