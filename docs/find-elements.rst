.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Find Elements
    :keywords: splinter, python, tutorial, find, selectors

+++++++++++++
Find Elements
+++++++++++++

Find Methods
============

Splinter's browser provides 8 methods for finding elements.

Example
-------

Given the following HTML:

.. highlight:: html

::

    <input type="button" id="btn_13" name="clickMeBtn" value="Click Me!">Do it!</input>

The following methods will find the element:

.. highlight:: python

::

    from splinter import Browser


    browser = Browser()

    elems = browser.find_by_css('#btn_13')
    elems = browser.find_by_xpath("//input[@id='btn_13']")
    elems = browser.find_by_tag('input')
    elems = browser.find_by_name('clickMeBtn')
    elems = browser.find_by_text('Do it!')
    elems = browser.find_by_id('btn_13')
    elems = browser.find_by_value('Click Me!')
    elems = browser.find('clickMeBtn')


Each of these methods returns an :ref:`ElementList <element-list>` with all matching elements.

browser.find()
--------------

Unlike the other finder methods, ``browser.find()`` does not specify the strategy used.
By default, it searches for an element by `name`.

This can be can changed to `css` or `xpath` using the ``browser.set_find_strategy()`` method.

.. highlight:: python

::

    from splinter import Browser


    browser = Browser()
    browser.set_find_strategy('css')

    elems = browser.find('#btn_13')

This will stay in effect for the entire life cycle of your script, unless
explicitly changed again.

Although ``browser.find()`` has a less implicit naming structure, it's also less verbose.
If the majority of your selectors use the same strategy it can improve the readability of your script.

Find Within Elements
====================

Elements implement the same finder methods as the browser.
The only difference being the root of the find operation.
Only child elements of the root element will be searched for.

.. highlight:: python

::

    from splinter import Browser


    browser = Browser()

    all_divs = browser.find_by_tag("div")
    child_elements = all_divs.first.find_by_css(".item")

Find Links
==========

To target only links on a page, the ``links`` namespace provides find 4 methods.
This is available at both the browser and element level.

Example
-------

Given the following HTML:

.. highlight:: html

::

    <div class="main">
        <a href="http://example.com">Link for Example.com</a>
    </div>

The following methods will find the element:

.. highlight:: python

::

    from splinter import Browser


    browser = Browser()

    links_found = browser.links.find_by_text('Link for Example.com')
    links_found = browser.links.find_by_partial_text('for Example')
    links_found = browser.links.find_by_href('http://example.com')
    links_found = browser.links.find_by_partial_href('example')

    elem = browser.find_by_css('.main').first
    links_found = my_element.links.find_by_text('Link for Example.com')
    links_found = my_element.links.find_by_partial_text('for Example.com')
    links_found = my_element.links.find_by_href('http://example.com')
    links_found = my_element.links.find_by_partial_href('example')


As the other ``find_*`` methods, these return an :ref:`ElementList <element-list>`.


ElementList
===========
.. _element-list:

These objects are functionally similar to Python's list object,
but with a few differences:

Get the first found element with the ``first`` attribute:

.. highlight:: python

::

    first_found = browser.find('clickMeBtn').first

Get the last found element with ``last`` attribute:

.. highlight:: python

::

    last_found = browser.find('clickMeBtn').last

Get by index:

.. highlight:: python

::

    second_found = browser.find('clickMeBtn')[1]


Handling Empty Lists
--------------------

If an element is not found, the element finding methods return an empty ElementList.
If you try to access items in this list, a
:class:`splinter.exceptions.ElementDoesNotExist` exception will be raised.

Further Reading
---------------

For more details see the API reference for the :class:`ElementList <splinter.element_list.ElementList>` class.
