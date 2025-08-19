.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Execute JavaScript In The Browser
    :keywords: splinter, python, tutorial, javascript

++++++++++++++++++
Execute JavaScript
++++++++++++++++++

When using WebDriver-based drivers, you can run JavaScript inside the web
browser.

Execute
=======

The `execute_script()` method takes a string containing JavaScript code and
executes it.

JSON-serializable objects and WebElements can be sent to the browser and used
by the JavaScript.

Examples
--------

Change the Background Color of an Element
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. highlight:: python

::

    browser = Browser()

    browser.execute_script(
      "document.querySelector('body').setAttribute('style', 'background-color: red')",
    )

Sending a WebElement to the browser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. highlight:: python

::

    browser = Browser()

    elem = browser.find_by_tag('body').first
    browser.execute_script(
      "arguments[0].setAttribute('style', 'background-color: red')",
      elem,
    )



Evaluate
========

The `evaluate_script()` method takes a string containing a JavaScript
expression and runs it, then returns the result.

JSON-serializable objects and WebElements can be sent to the browser and used
by the JavaScript.

Examples
--------

Get the href from the browser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. highlight:: python

::

    browser = Browser()

    href = browser.evaluate_script("document.location.href")


Cookbook
========

Manipulate text fields with JavaScript
--------------------------------------

Some text input actions cannot be "typed" thru ``browser.fill()``, like new lines and tab characters.
Below is en example how to work around this using ``browser.execute_script()``.
This is also much faster than ``browser.fill()`` as there is no simulated key typing delay, making it suitable for longer texts.

::

   def fast_fill(browser, query: str, text: str):
       """Fill text field with copy-paste, not by typing key by key.

       Otherwise you cannot type enter or tab.

       Arguments:
          query: CSS id of the textarea element to fill
       """
       text = text.replace("\t", "\\t")
       text = text.replace("\n", "\\n")

       elem = browser.find_by_css(query).first
       # Construct a JavaScript snippet that is executed on the browser side
       script = f"arguments[0].value = "{text}";"
       browser.execute_script(script, elem)
