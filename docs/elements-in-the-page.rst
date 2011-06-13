.. meta::
    :description: Dealing with elements in the page.
    :keywords: splinter, python, tutorial, documentation, forms, click links, get value

+++++++++++++++++++++++++++++++++++++
Interacting with elements in the page
+++++++++++++++++++++++++++++++++++++

Get value of an element
-----------------------

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

