.. meta::
    :description: Documentation for splinter, an open source tool for testing web applications
    :keywords: splinter, python, tutorial, documentation, web application, tests, atdd, tdd, acceptance tests


+++++++++++++++++++++++++++++++++++++++++++++
automate web application actions using python
+++++++++++++++++++++++++++++++++++++++++++++

`what's new in splinter 0.0.3? <http://splinter.cobrateam.info/docs/news.html>`_

first steps
===========

* `Installation <http://splinter.cobrateam.info/docs/install.html>`_
* `Quick tutorial <http://splinter.cobrateam.info/docs/tutorial.html>`_


* `Finding elements <http://splinter.cobrateam.info/docs/finding.html>`_

splinter opensource project
===========================

* `Community <http://splinter.cobrateam.info/docs/community.html>`_
* `Contribute <http://splinter.cobrateam.info/docs/contribute.html>`_


documentation
=============

Browser
-------

To use splinter you need create a Browser instance:

.. highlight:: python

::

    from splinter.browser import Browser
    browser = Browser()


splinter support three drivers: chrome, firefox and zopetestbrowser

.. highlight:: python

::

    browser = Browser('webdriver.chrome')
    browser = Browser('webdriver.firefox')
    browser = Browser('zope.testbrowser')

Navigating with Browser.visit
-----------------------------

You can use the ``visit`` method to navigate to other pages:

.. highlight:: python

::

    browser.visit('http://cobrateam.info')

The ``visit`` method takes only a single parameter - the ``url`` to be visited.

Reload a page
-------------

You can reload a page using ``reload`` method:

.. highlight:: python

::

    browser.reload()

Navigate through the history
----------------------------

You can back and forward on your browsing history using ``back`` and ``forward`` methods:

.. highlight:: python

::

    browser.visit('http://cobrateam.info')
    browser.visit('http://splinter.cobrateam.info')
    browser.back()
    browser.forward()

..

    **Note:** This feature is not supported yet on Chrome driver.

Dealing with HTTP status code
-----------------------------

It's also possible to check which HTTP status code a browser.visit gets. You can use ``status_code.is_success`` to do the work
for you or you can compare the status code directly:

.. highlight:: python

::

    browser.visit('http://cobrateam.info')
    browser.status_code.is_success() # True
    # or
    browser.status_code == 200 # True

The difference between those methods is that if you get a redirect (or something that is not an HTTP error),
``status_code.is_success`` will consider your response as successfully.

Handling HTTP exceptions
------------------------

Whenever you use the ``visit`` method, Splinter will check if the response is success or not, and if not, it will raise an
HttpResponseError exception. But don't worry, you can easily catch it:

.. highlight:: python

::

    try:
        browser.visit('http://cobrateam.info/i-want-cookies')
    except HttpResponseError, e:
        print "Oops, I failed with the status code %s and reason %s" % (e.status_code, e.reason)

..

    **Note:** ``status_code`` and this HTTP exception handling is available only for selenium webdriver

Browser.title
-------------

You can get the title of the visited page using the ``title`` attribute:

.. highlight:: python

::

    browser.title

Verifying page content with Browser.html
----------------------------------------

You can use the ``html`` attribute to get the html content of the visited page:

.. highlight:: python

::

    browser.html

Verifying page url with Browser.url
-----------------------------------

The visited page's url can be accessed by the ``url`` attribute:

.. highlight:: python

::

    browser.url

Get element value
-----------------

In order to retrieve an element's value, use the ``value`` property:

.. highlight:: python

::

    browser.find_by_css('h1').first.value

or

.. highlight:: python

::

    element = browser.find_by_css('h1').first
    element.value


Clicking links
--------------

You can click in links. To click in links by href or text you can use this.
IMPORTANT: This methods return the first element always.

.. highlight:: python

::

    browser.click_link_by_href('/my_link')

or

.. highlight:: python

::

    browser.click_link_by_text('my link')


Clicking buttons
----------------

You can click in buttons. Splinter follows any redirects, and submits forms associated with buttons.

.. highlight:: python

::

    browser.find_by_name('send').first.click()

or

.. highlight:: python

::

    browser.find_link_by_text('my link').first.click()


Interacting with forms
----------------------

.. highlight:: python

::

    browser.fill('query', 'my name')
    browser.attach_file('file', '/path/to/file/somefile.jpg')
    browser.choose('some-radio')
    browser.check('some-check')
    browser.uncheck('some-check')
    browser.select('uf', 'rj')

Verifying if element is visible or invisible
--------------------------------------------

To check if an element is visible or invisible, use the ``visible`` property. For instance:

.. highlight:: python

::

    browser.find_by_css('h1').first.visible

will be True if the element is visible, or False if it is invisible.

Ajax and async javascript
-------------------------

When working with ajax and async javascript, it's common you work with with an element which is not yet present on the page.

splinter have methods for verifying if element is present in a page, that wait for a element and returns `True` if element is present:

.. highlight:: python

::

    browser.is_element_present_by_css('h1')
    browser.is_element_present_by_xpath('//h1')
    browser.is_element_present_by_tag('h1')
    browser.is_element_present_by_name('name')
    browser.is_element_present_by_id('firstheader')

You can verify too if element is not present in a page:

.. highlight:: python

::

    browser.is_element_not_present_by_css('h1')
    browser.is_element_not_present_by_xpath('//h1')
    browser.is_element_not_present_by_tag('h1')
    browser.is_element_not_present_by_name('name')
    browser.is_element_not_present_by_id('firstheader')


Executing javascript
--------------------

You can easily execute JavaScript, in drivers which support it:

.. highlight:: python

::

    browser.execute_script("$('body').empty()")

You can return the result of the script:

.. highlight:: python

::

    browser.evaluate_script("4+4") == 8


Using iframes
-------------------------

You can use the ``get_iframe`` method and the ``with`` statement to interact with iframes.

.. highlight:: python

::

    with browser.get_iframe('iframemodal') as iframe:
        iframe.do_stuff()


Handling alerts and prompts
----------------------------

IMPORTANT: Only Firefox webdriver has support for alerts and prompts.
Calling any of the following methods from other webdriver (like Chrome) will raise NotImplementedError.

You can deal with alerts and prompts using the ``get_alert`` method.

.. highlight:: python

::

    alert = browser.get_alert()
    alert.text
    alert.accept()
    alert.dismiss()


In case of prompts, you can answer it using the ``fill_with`` method.

.. highlight:: python

::

    prompt = browser.get_alert()
    prompt.text
    prompt.fill_with('text')
    prompt.accept()
    prompt.dismiss()


You can use the ``with`` statement to interacte with both alerts and prompts too.

.. highlight:: python

::

    with browser.get_alert() as alert:
        alert.do_stuff()

If there's not any prompt or alert, ``get_alert`` will return ``None``.
Remember to always use at least one of the alert/prompt ending methods (accept and dismiss).
Otherwise your browser instance will be frozen until you accept or dismiss the alert/prompt correctly.
