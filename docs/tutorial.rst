+++++++++++++++++
Splinter Tutorial
+++++++++++++++++

This guide assumes your machine meets the requirements outlined in the Installation section of this documentation.

In this guide let's search about splinter in the google.com and verify that splinter website is found.

Create a browser instance
=========================

First it's need import a Browser class and create a browser instance. 

::
    from splinter.browser import Browser
    browser = Browser()


Visiting a web page
===================

Using the browser instance you can visit web page, using ``browser.visit`` method:

::

    browser.visit('http://google.com')


Make your actions
=================

After the page is loaded, you can make actions, like click's, fill text input, check radio and checkbox. Let's fill a text input for our search.

::

    browser.fill('q', 'splinter - python acceptance testing for web applications')

Finding elelments
=================

You can find elements in page using css, xpath, id, tag or name how selector. Let's find and click in search button for make a search.

::

    browser.find_by_css('.lsb').first.click()


Verify if expect text or element is present
===========================================

Now, it's possible verify that splinter website url is present in the page.

::

    'http://splinter.cobrateam.info' in browser.html


Closing the browser
===================

And for close the browser, use the ``browser.close``:

::

    browser.quit()

