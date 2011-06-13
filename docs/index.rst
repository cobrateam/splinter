.. meta::
    :description: Documentation for splinter, an open source tool for testing web applications
    :keywords: splinter, python, tutorial, documentation, web application, tests, atdd, tdd, acceptance tests


+++++++++++++++++++++++++++++++++++++++++++++
automate web application actions using python
+++++++++++++++++++++++++++++++++++++++++++++

:doc:`what's new in splinter 0.0.3? </news>`

First steps
===========

Getting started
---------------

* :doc:`Installation </install>`
* :doc:`Setup Google Chrome driver </setup-chrome>`
* :doc:`Quick tutorial </tutorial>`

Walking on...
-------------

* :doc:`Browser </browser>`
* :doc:`Finding elements </finding>`
* :doc:`Execute javascript </javascript>`
* :doc:`Interacting with iframes, alerts and prompts </iframes-and-alerts>`

splinter open source project
============================

* :doc:`Community </community>`
* :doc:`Contribute </contribute>`


documentation
=============

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
