.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

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


Example: manipulating text fields with JavaScript
+++++++++++++++++++++++++++++++++++++++++++++++++

Some text input actions cannot be "typed" thru ``browser.fill()``, like new lines and tab characters. Below is en example how to work around this using ``browser.execute_script()``. This is also much faster than ``browser.fill()`` as there is no simulated key typing delay, making it suitable for longer texts.

::

   def fast_fill_by_javascript(browser: DriverAPI, elem_id: str, text: str):
       """Fill text field with copy-paste, not by typing key by key.

       Otherwise you cannot type enter or tab.

       :param id: CSS id of the textarea element to fill
       """
       text = text.replace("\t", "\\t")
       text = text.replace("\n", "\\n")

       # Construct a JavaScript snippet that is executed on the browser sdie
       snippet = f"""document.querySelector("#{elem_id}").value = "{text}";"""
       browser.execute_script(snippet)
