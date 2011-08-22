.. meta::
    :description: Finding elements
    :keywords: splinter, python, tutorial, find, selectors

++++++++++++++++
Finding elements
++++++++++++++++

For finding elements you can use six methods, one for each selector type ``css``, ``xpath``, ``tag``, ``name``, ``id``, ``value``:

.. highlight:: python

::

    browser.find_by_css('h1')
    browser.find_by_xpath('//h1')
    browser.find_by_tag('h1')
    browser.find_by_name('name')
    browser.find_by_id('firstheader')
    browser.find_by_value('query')

These methods returns a list of all found elements.


you can get the first found element:

.. highlight:: python

::

    browser.find_by_name('name').first

You can use too the last attribute, that returns the last found element:

.. highlight:: python

::

    browser.find_by_name('name').last

Get element using index
=======================

You also use index for get a element

.. highlight:: python

::

    browser.find_by_name('name')[1]

all elements and find_by_id
===========================

A web page should be only one id per page. Then find_by_id() method return always a list with one element.

Finding links
=============

For finding link elements you can use ``find_link_by_text``, ``find_link_by_partial_text``, ``find_link_by_href`` or ``find_link_by_partial_href``:

.. highlight:: python

::

    browser.find_link_by_text('Link for Example.com')

or

.. highlight:: python

::

    browser.find_link_by_partial_text('for Example')

or

.. highlight:: python

::

    browser.find_link_by_href('http://example.com')

or

.. highlight:: python

::

    browser.find_link_by_partial_href('example')

These methods returns a list of all found elements.

For finding links by id, tag, name or xpath you should use other find methods (``find_by_css``, ``find_by_xpath``, ``find_by_tag``, ``find_by_name``, ``find_by_value`` and ``find_by_id``).

Chaining find of elements
=========================

Finding methods are chainable, so you can find the descendants of a previously found element.

.. highlight:: python

::

    elements = browser.find_by_css("div")
    within_elements = elements.first.find_by_name("name")

Element not found exception
===========================

If element not found, find methods returns a empty list. But, if you try, access a element in list raises the :class:`splinter.exceptions.ElementDoesNotExist` exception.
