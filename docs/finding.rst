.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Finding elements
    :keywords: splinter, python, tutorial, find, selectors

++++++++++++++++
Finding elements
++++++++++++++++

Splinter provides 6 methods for finding elements in the page, one for each
selector type: ``css``, ``xpath``, ``tag``, ``name``, ``id``, ``value``.
Examples:

.. highlight:: python

::

    browser.find_by_css('h1')
    browser.find_by_xpath('//h1')
    browser.find_by_tag('h1')
    browser.find_by_name('name')
    browser.find_by_id('firstheader')
    browser.find_by_value('query')


Each of these methods returns a list with the found elements. You can get the
first found element with the ``first`` shortcut:

.. highlight:: python

::

    first_found = browser.find_by_name('name').first

There's also the ``last`` shortcut -- obviously, it returns the last found
element:

.. highlight:: python

::

    last_found = browser.find_by_name('name').last


Get element using index
=======================

You also can use an index to get the desired element in the list of found
elements:

.. highlight:: python

::

    second_found = browser.find_by_name('name')[1]

All elements and ``find_by_id``
===============================

A web page should have only one id, so the ``find_by_id`` method returns always
a list with just one element.

Finding links
=============

If you need to find the links in a page, you can use the methods
``find_link_by_text``, ``find_link_by_partial_text``, ``find_link_by_href`` or
``find_link_by_partial_href``. Examples:

.. highlight:: python

::

    links_found = browser.find_link_by_text('Link for Example.com')
    links_found = browser.find_link_by_partial_text('for Example')
    links_found = browser.find_link_by_href('http://example.com')
    links_found = browser.find_link_by_partial_href('example')


As the other ``find_*`` methods, these returns a list of all found elements.

You also can search for links using other selector types with the methods 
``find_by_css``, ``find_by_xpath``, ``find_by_tag``, ``find_by_name``,
``find_by_value`` and ``find_by_id``.

Chaining find of elements
=========================

Finding methods are chainable, so you can find the descendants of a previously
found element.

.. highlight:: python

::

    divs = browser.find_by_tag("div")
    within_elements = divs.first.find_by_name("name")

``ElementDoesNotExist`` exception
=================================

If an element is not found, the ``find_*`` methods returns an empty list. But
if you try to access an element in this list, it will raise the
:class:`splinter.exceptions.ElementDoesNotExist` exception.
