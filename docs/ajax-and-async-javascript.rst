.. meta::
    :description: AJAX and asynchorous JavaScript
    :keywords: splinter, python, tutorial, javascript, ajax, waiting

++++++++++++++++++++++++++++++++
AJAX and asynchronous JavaScript
++++++++++++++++++++++++++++++++

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
