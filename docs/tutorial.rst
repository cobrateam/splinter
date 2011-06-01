+++++++++++++++++
Splinter Tutorial
+++++++++++++++++

Before starting, make sure Splinter is `installed <http://splinter.cobrateam.info/docs/install.html>`_.

This tutorial provides a simple example, teaching step by step how to:

* search for ``splinter - python acceptance testing for web applications'`` in google.com, and
* find if splinter official website is listed among the search results

Create a Browser instance
=========================

First of all, import ``Browser`` class and instantiate it. 

::

    from splinter.browser import Browser
    browser = Browser()


Visit Google website
====================

Visit any website using the ``browser.visit`` method. Let's go to Google search page:

::

    browser.visit('http://google.com')


Input search text
=================

After a page is loaded, you can perform actions, such as clicking, filling text input, checking radio and checkbox. Let's fill Google's search field with ``splinter - python acceptance testing for web applications``:

::

    browser.fill('q', 'splinter - python acceptance testing for web applications')

Press the search button
=======================

Tell Splinter which button should be pressed. A button - or any other element - can be identified using its css, xpath, id, tag or name.

In order to find Google's search button, do:

::

    button = browser.find_by_css('.lsb').first

Note that this ``.lsb`` was found looking at Google's page source code.

With the button in hands, we can then press it:

::

    button.first.click()


Note: Both steps presented above could be joined in a single line, such as:

::

    browser.find_by_css('.lsb').first.click()


Find out that Splinter official website is in the search results
================================================================

After pressing the button, you can check if Splinter official website is among the search responses. This can be done like this:

::

    if browser.is_text_present('http://splinter.cobrateam.info'):
        print "Yes, found it! :)"
    else:
        print "No, didn't find it :("


In this case, we are just printing something. You might use assertions, if you're writing tests.

Close the browser
=================

When you've finished testing, close your browser using ``browser.quit``:

::

    browser.quit()

All together
============

Finally, the source code will be:

::

    from splinter.browser import Browser

    browser = Browser()
    browser.visit('http://google.com')
    browser.fill('q', 'splinter - python acceptance testing for web applications')
    browser.find_by_css('.lsb').first.click()

    if browser.is_text_present('http://splinter.cobrateam.info'):
        print 'Yes, the official website was found!'
    else:
        print 'No, it wasn't found... We need to improve the SEO'

    browser.quit()

