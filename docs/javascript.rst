.. meta::
    :description: Executing javascript 
    :keywords: splinter, python, tutorial, javascript

++++++++++++++++++++
Executing javascript
++++++++++++++++++++

You can easily execute JavaScript, in drivers which support it:

.. highlight:: python

::

    browser.execute_script("$('body').empty()")

You can return the result of the script:

.. highlight:: python

::

    browser.evaluate_script("4+4") == 8


