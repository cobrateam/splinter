.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Automatic interaction with alerts, prompts and iframes
    :keywords: splinter, python, tutorial, alerts, prompts, iframes, acceptance tests

++++++++++++++++++++++++++
Frames, alerts and prompts
++++++++++++++++++++++++++

Using iframes
-------------

You can use the ``get_iframe`` method and the ``with`` statement to interact with iframes. You can pass the iframe's name, id, index, or web element to ``get_iframe``.

.. highlight:: python

::

    with browser.get_iframe('iframemodal') as iframe:
        iframe.do_stuff()


Handling alerts and prompts
---------------------------

    Chrome support for alerts and prompts is new in Splinter 0.4.

**IMPORTANT:** Only webdriver (Firefox and Chrome) has support for alerts and prompts.

You can interact with alerts and prompts using the ``get_alert`` method.

.. highlight:: python

::

    alert = browser.get_alert()
    alert.text
    alert.accept()
    alert.dismiss()


In case of prompts, you can answer it using the ``send_keys`` method.

.. highlight:: python

::

    prompt = browser.get_alert()
    prompt.text
    prompt.send_keys('text')
    prompt.accept()
    prompt.dismiss()


You can also use the ``with`` statement to interact with both alerts and prompts.

.. highlight:: python

::

    with browser.get_alert() as alert:
        alert.do_stuff()

If there's no prompt or alert, ``get_alert`` will return ``None``.
Remember to always use at least one of the alert/prompt ending methods (accept and dismiss).
Otherwise, your browser instance will be frozen until you accept or dismiss the alert/prompt correctly.
