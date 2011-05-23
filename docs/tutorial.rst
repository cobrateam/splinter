+++++++++++++++++
Splinter Tutorial
+++++++++++++++++

This guide assumes your machine meets the requirements outlined in the Installation section of this documentation.

Create a browser instance
=========================

First it's need create a browser instance. 

::

    browser = Browser()


Visiting a web page
===================

Using the browser instance you can visit web page, using ``browser.visit`` method:

::

    browser.visit('http://google.com')


Make your actions
=================

After the page is loaded, you can make actions, like click's, fill text input, check radio and checkbox:

::

    browser.fill('q', 'splinter test tool')
    browser.click('')


Finding expected elements
=========================

You can find elements in page using css, xpath, id, tag or name how selector:

::

    print browser.find_by_css('').first


Closing the browser
===================

And for close the browser, use the ``browser.close``:

::

    browser.close()

