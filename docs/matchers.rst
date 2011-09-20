.. meta::
    :description: Verifying if a texxt pattern is or not present
    :keywords: splinter, python, tutorial, element

++++++++
Matchers
++++++++

There are two kind of methods to verify the presence of texts and elements in a page: "is_element_present" and "is_text_present".
When working with ajax and async javascript, it's common you work with an element which is not yet present on the page.

To use these methods you give the element or text to be found.
There is also the opcional "wait_time" argument which is given the time in seconds.
If the "wait_time" is given and the verification method gets True it will return the result, even if the wait_time is not over,
and if it doesn't gets True, the method will wait until the wait_time is over to return the result.


Verifying text presence
-----------------------

There's one method responsible for checking whether a text is present on the page content, the ``is_text_present`` method.

This method returns a boolean value, True if is present and False if is not present.

.. highlight:: python

::

    browser = Browser()
    browser.visit('http://splinter.cobrateam.info/')
    browser.is_text_present('splinter') # true
    browser.is_text_present('splinter', wait_time=10) # true, using wait_time
    browser.is_text_present('text not present') # false

There's also the method to verify if the test is not present, the ``is_text_not_present`` method.

This method also returns a boolean value, True if is not present and False if is present.

.. highlight:: python

::

    browser.is_text_not_present('text not present') # true
    browser.is_text_not_present('text not present', wait_time=10) # true, using wait_time
    browser.is_text_not_present('splinter') # false


Verifying elements presence
---------------------------

For verifying the elements presence you can use six methods, one for each selector type ``css``, ``xpath``, ``tag``, ``name``, ``id``, ``value``:
Verifying if the element is present:

.. highlight:: python

::

    browser.is_element_present_by_css('h1')
    browser.is_element_present_by_xpath('//h1')
    browser.is_element_present_by_tag('h1')
    browser.is_element_present_by_name('name')
    browser.is_element_present_by_id('firstheader')
    browser.is_element_present_by_value('query')
    browser.is_element_present_by_value('query', wait_time=10) # using wait_time

These methods returns True if the element is present and False if is not present.


Verifying if the element is not present:

.. highlight:: python

::

    browser.is_element_not_present_by_css('h6')
    browser.is_element_not_present_by_xpath('//h6')
    browser.is_element_not_present_by_tag('h6')
    browser.is_element_not_present_by_name('unexisting-name')
    browser.is_element_not_present_by_id('unexisting-header')
    browser.is_element_not_present_by_id('unexisting-header', wait_time=10) # using wait_time
