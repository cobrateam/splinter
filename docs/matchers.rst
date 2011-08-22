.. meta::
    :description: Verifying if a texxt pattern is or not present
    :keywords: splinter, python, tutorial, element


+++++++++++++++++++++++
Verifying text presence
+++++++++++++++++++++++

There's one method responsible for checking whether a text is present on the page content, the ``is_text_present`` method.

This method returns a boolean value, True if is present and False if is not present.

.. highlight:: python

::

    browser = Browser()
    browser.visit('http://splinter.cobrateam.info/')
    browser.is_text_present('splinter') # true
    browser.is_text_present('text not present') # false

There's also the method to verify if the test is not present, the ``is_text_not_present`` method.

This method also returns a boolean value, True if is not present and False if is present.

.. highlight:: python

::

    browser.is_text_not_present('text not present') # true
    browser.is_text_not_present('splinter') # false
