.. meta::
    :description: Automatic interaction with alerts, prompts and iframes
    :keywords: splinter, python, tutorial, alerts, prompts, iframes, acceptance tests

++++++++++++++++++++++++++
Frames, alerts and prompts
++++++++++++++++++++++++++

Using iframes
-------------

You can use the ``get_iframe`` method and the ``with`` statement to interact with iframes.

.. highlight:: python

::

    with browser.get_iframe('iframemodal') as iframe:
        iframe.do_stuff()


Handling alerts and prompts
---------------------------

IMPORTANT: Only Firefox webdriver has support for alerts and prompts.
Calling any of the following methods from other webdriver (like Chrome) will raise NotImplementedError.

You can deal with alerts and prompts using the ``get_alert`` method.

.. highlight:: python

::

    alert = browser.get_alert()
    alert.text
    alert.accept()
    alert.dismiss()


In case of prompts, you can answer it using the ``fill_with`` method.

.. highlight:: python

::

    prompt = browser.get_alert()
    prompt.text
    prompt.fill_with('text')
    prompt.accept()
    prompt.dismiss()


You can use the ``with`` statement to interacte with both alerts and prompts too.

.. highlight:: python

::

    with browser.get_alert() as alert:
        alert.do_stuff()

If there's not any prompt or alert, ``get_alert`` will return ``None``.
Remember to always use at least one of the alert/prompt ending methods (accept and dismiss).
Otherwise your browser instance will be frozen until you accept or dismiss the alert/prompt correctly.
