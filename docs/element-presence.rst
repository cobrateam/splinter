.. meta::
    :description: Verifying if a element is present or not present
    :keywords: splinter, python, tutorial, element

+++++++++++++++++++++++++++
Verifying elements presence
+++++++++++++++++++++++++++

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

These methods returns True if the element is present and False if is not present.


Verifying if the element is not present:

.. highlight:: python

::

    browser.is_element_not_present_by_css('h6')
    browser.is_element_not_present_by_xpath('//h6')
    browser.is_element_not_present_by_tag('h6')
    browser.is_element_not_present_by_name('unexisting-name')
    browser.is_element_not_present_by_id('unexisting-header')

These methods returns True if the element is not present and False if is present.
