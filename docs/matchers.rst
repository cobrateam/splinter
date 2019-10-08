.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Checking if a text pattern is or not present
    :keywords: splinter, python, tutorial, element

++++++++
Matchers
++++++++

When working with AJAX and asynchronous JavaScript, it's common to have
elements which are not present in the HTML code (they are created with
JavaScript, dynamically). In this case you can use the methods
``is_element_present`` and ``is_text_present`` to check the existence of an
element or text -- Splinter will load the HTML and JavaScript in the browser
and the check will be performed *before* processing JavaScript.

There is also the optional argument ``wait_time`` (given in seconds) -- it's a
timeout: if the verification method gets ``True`` it will return the result
(even if the ``wait_time`` is not over), if it doesn't get ``True``, the
method will wait until the ``wait_time`` is over (so it'll return the result).


Checking the presence of text
-----------------------------

The method ``is_text_present`` is responsible for checking if a text is present
in the page content. It returns ``True`` or ``False``.

.. highlight:: python

::

    browser = Browser()
    browser.visit('https://splinter.readthedocs.io/')
    browser.is_text_present('splinter') # True
    browser.is_text_present('splinter', wait_time=10) # True, using wait_time
    browser.is_text_present('text not present') # False


There's also a method to check if the text *is not* present:
``is_text_not_present``. It works the same way but returns ``True`` if the text
is not present.

.. highlight:: python

::

    browser.is_text_not_present('text not present') # True
    browser.is_text_not_present('text not present', wait_time=10) # True, using wait_time
    browser.is_text_not_present('splinter') # False


Checking the presence of elements
---------------------------------

Splinter provides 6 methods to check the presence of elements in the page, one
for each selector type: ``css``, ``xpath``, ``tag``, ``name``, ``id``,
``value``, ``text``. Examples:

.. highlight:: python

::

    browser.is_element_present_by_css('h1')
    browser.is_element_present_by_xpath('//h1')
    browser.is_element_present_by_tag('h1')
    browser.is_element_present_by_name('name')
    browser.is_element_present_by_text('Hello World!')
    browser.is_element_present_by_id('firstheader')
    browser.is_element_present_by_value('query')
    browser.is_element_present_by_value('query', wait_time=10) # using wait_time

As expected, these methods returns ``True`` if the element is present and
``False`` if it is not present.

There's also the negative forms of these methods, as in ``is_text_present``:

.. highlight:: python

::

    browser.is_element_not_present_by_css('h6')
    browser.is_element_not_present_by_xpath('//h6')
    browser.is_element_not_present_by_tag('h6')
    browser.is_element_not_present_by_name('unexisting-name')
    browser.is_element_not_present_by_text('Not here :(')
    browser.is_element_not_present_by_id('unexisting-header')
    browser.is_element_not_present_by_id('unexisting-header', wait_time=10) # using wait_time


Checking the visibility of elements
---------------------------------

There are two methods to check if the element is visible or hidden in the current page using either the selector type ``css`` or ``xpath``. It 
returns ``True`` if the element is visible and ``False`` if the element in not visible.  

.. highlight:: python

::

    browser.is_element_visible_by_css('h5') 
    browser.is_element_visible_by_css('h5', wait_time=10) 
    browser.is_element_visible_by_xpath('//h5')

