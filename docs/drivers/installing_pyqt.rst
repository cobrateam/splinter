.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Learn how to install PyQt4 on your machine.
    :keywords: splinter, python, cobrateam, pyqt, pyqt4

++++++++++++++++
Installing PyQt4
++++++++++++++++

In order to use Spynner driver, you need to install PyQt4. PyQt4 itself has a few dependencies;
follow the steps below to get PyQt4 and its dependencies running on your system.

Install Qt4
===========

The biggest and most important PyQt4 dependency is the Qt4 itself.
You can download it from its `official website <http://qt.nokia.com/downloads/>`_ and
install with a nice and friendly wizard.

Install SIP
===========

Another PyQt4 dependency is `SIP <http://www.riverbankcomputing.co.uk/software/sip/intro>`_, which
is a tool used to create Python bindings for C and C++ libraries. You can navigate to the
`download page on SIP website <http://www.riverbankcomputing.co.uk/software/sip/download>`_,
choose the version according to your operating system, extract the download package and
install it using three commands:

.. highlight:: bash

::

    $ tar -xvzf sip-4.xx.x.tar.gz
    $ cd sip-4.xx.x
    $ python configure.py
    $ make
    $ [sudo] make install

Install PyQt4
=============

Now we can finally install PyQt4. Go to the `PyQt4 download page <http://www.riverbankcomputing.co.uk/software/pyqt/download>`_
and download the PyQt4 version according to your platform. After these steps, all you need to do is extract the download
package and install PyQt4 using these commands:

.. highlight:: bash

::

    $ tar -xvzf PyQt-plat-gpl-4.x.x.tar.gz
    $ cd PyQt-plat-gpl-4.x.x
    $ python configure.py --no-designer-plugin --qmake=/usr/bin/qmake-4.x # important, on Mac OS X don't use /usr/bin/qmake, specify the version!
    $ make
    $ [sudo] make install

Now you PyQt4 installed on your system. Happy hacking :)

For more information in specific platforms, check these links out:

    * `Installing PyQt on Mac OS X (Snow Leopard) <http://blog.oak-tree.us/index.php/2010/05/27/pyqt-snow-leopard>`_
    * `Installing PyQt on Windows <http://blog.oak-tree.us/index.php/2009/05/12/pyqt-windows>`_
    * `Installing PyQt on Linux (Ubuntu) <http://blog.oak-tree.us/index.php/2009/05/12/pyqt-linux>`_
