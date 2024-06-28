.. Copyright 2024 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Keyboard
    :keywords: splinter, python, tutorial, documentation, selenium integration, selenium keys, keyboard events

++++++++
Keyboard
++++++++

The browser provides an interface for using the keyboard. This triggers
keyboard events inside the current browser window.

.. note:: Input detection is limited to the page. You cannot control the browser
  or your operating system directly using the keyboard.

The keyboard interface is generally used to trigger modifier keys.
For text input, using the keyboard is not recommended. Instead, use the
:func:`element.fill() <splinter.driver.ElementAPI.fill>` method.

.. note:: The control modifier key is different across operating systems.
  e.g.: macOS uses `COMMAND` and Windows & Linux use `CONTROL`.
  For a cross-platform solution, `CTRL` can be used and will be resolved
  for you.

Actions
=======

Down
----

Hold a key down.

.. code-block:: python

    from splinter import Browser


    browser = Browser()
    browser.visit("https://duckduckgo.com/")
    browser.keyboard.down("CONTROL")


Up
--

Release a key. If the key is not held down, this will do nothing.

.. code-block:: python

    from splinter import Browser


    browser = Browser()
    browser.visit("https://duckduckgo.com/")
    browser.keyboard.down("CONTROL")
    browser.keyboard.up("CONTROL")


Press
-----

Hold and then release a key pattern.

.. code-block:: python

    from splinter import Browser


    browser = Browser()
    browser.visit("https://duckduckgo.com/")
    browser.keyboard.press("CONTROL")

Key patterns are keys separated by the '+' symbol.
This allows multiple presses to be chained together:

.. code-block:: python

    from splinter import Browser


    browser = Browser()
    browser.visit("https://duckduckgo.com/")
    browser.keyboard.press("CONTROL+a")

.. warning::
  Although a key pattern such as "SHIFT+awesome" will be accepted,
  the press method is designed for single keys. There may be unintended
  side effects to using it in place of Element.fill() or Element.type().

Press Using a Context Manager
-----------------------------

Using the `pressed()` method, a context manager will be invoked.
The specified key will be held down, then released when the block is exited.

.. code-block:: python

    from splinter import Browser


    browser = Browser()
    browser.visit("https://duckduckgo.com/")
    with browser.keyboard.pressed("SHIFT"):
        browser.find_by_css("[@name='q']").fill('splinter')


Element.press()
---------------

Elements can be pressed directly.

.. code-block:: python

    from splinter import Browser


    browser = Browser()
    browser.visit("https://duckduckgo.com/")
    elem = browser.find_by_css("#searchbox_input")
    elem.fill("splinter python")
    elem.press("ENTER")

    results = browser.find_by_xpath("//section[@data-testid='mainline']/ol/li")

    # Open in a new tab behind the current one.
    results.first.press("CONTROL+ENTER")

Cookbook
========

Copy & Paste
------------

.. code-block:: python

    browser.visit(https://duckduckgo.com/)

    elem = browser.find_by_css("#searchbox_input").first

    elem.fill("Let's copy this value")

    browser.keyboard.press("CTRL+a")
    browser.keyboard.press("CTRL+c")

    assert elem.value == ""

    elem.click()

    browser.keyboard.press("CTRL+v")

    assert elem.value == "Let's copy this value"
