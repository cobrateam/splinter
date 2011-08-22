.. meta::
    :description: Verifying if a texxt pattern is or not present
    :keywords: splinter, python, tutorial, element


+++++++++++++++++++++++
Verifying text presence
+++++++++++++++++++++++

There's one method responsible for checking whether a text is present on the page content, the ``is_text_present`` method.

This method returns a boolean value.

.. highlight:: python

::

    browser = Browser()
    browser.visit('http://splinter.cobrateam.info/')
    browser.is_text_present('splinter') # true
    browser.is_text_present('text not present') # false
