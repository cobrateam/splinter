+++++++++++++
Install guide
+++++++++++++

Install Python
==============

Being a Python testing tool, splinter requires Python. It works with any Python version from 2.5 to 2.7 (splinter does not currently work with Python 3.0).

Get Python at http://www.python.org. If you’re running Linux or Mac OS X, you probably already have it installed.

Install splinter
================

You've got two options to install splinter:

Install an official release
---------------------------

This is the best approach for users who want a stable version number.


::

	[sudo] pip install splinter



Install the development version
-------------------------------

This is best for users who want the latest-and-greatest features and aren't afraid of running brand-new code. 

Make sure that you have git installed, and that you can run its commands from a shell. (Enter git help at a shell prompt to test this.)

Check out git like so:


::

    git clone splinter
    cd splinter
    [sudo] python setup.py install
