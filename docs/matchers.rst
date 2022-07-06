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
-----------------------------------

Elements have two methods to check visibility.

.. highlight:: python

::

    browser.find_by_css('h5').is_visible()

    browser.find_by_css('h5').is_not_visible()


Unlike an element's `visible` attribute, which returns the current visibility status, these methods will poll the browser for a specified number of seconds looking for the desired state.

 Both methods:

  - Take an optional `wait_time` argument. If not specified, the browser's default wait_time will be used.
  - Return a boolean.


The difference between:

.. highlight:: python

::

    result = not browser.find_by_css('h5').is_visible()

and:

.. highlight:: python

::

    result = browser.find_by_css('h5').is_not_visible()

is when the method will return a value.
`not element.is_visible()` will look for a specified number of seconds for the element to be visible, eventually returning False.
`element.is_not_visible()` will look for a specified number of seconds for the element to not be visible, returning False the moment the condition is met.

As a result, `element.is_not_visible()` will always be faster than `not element.is_visible()`
