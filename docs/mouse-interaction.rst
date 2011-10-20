.. meta::
    :description: Mouse interatcion.
    :keywords: splinter, python, tutorial, documentation, mouse interaction, mouseover, mouseout, doube click, mouse events

++++++++++++++++++
Mouse interactions
++++++++++++++++++

    **Note:** Mouse interaction currently works only on Chrome driver.

Splinter provides some methods for mouse interactions with elements in the page.
This feature is useful to test if an element appears on mouse over and
disappears on mouse out (eg.: submitems of a menu).

It's also possible to send a click, double click or right click to the element.

Here is a simple example: imagine you have this `jQuery <http://jquery.com>`_
event for mouse over and out:

.. highlight:: js

::

    $('.menu-links').mouseover(function(){
        $(this).find('.subitem').show();
    });

    $('.menu-links').mouseout(function(){
        $(this).find('.subitem').hide();
    });

You can use Splinter to fire the event programatically:

.. highlight:: python

::

    browser.find_by_css('.menu-links').mouse_over()
    # Code to check if the subitem is visible...
    browser.find_by_css('.menu-links').mouse_out()


The methods available for mouse interactions are:

``mouse_over``
--------------

.. highlight:: python


Puts the mouse above the element. Example:

::

    browser.find_by_tag('h1').mouse_over()


``mouse_out``
-------------

.. highlight:: python

Puts the mouse out of the element. Example:

::

    browser.find_by_tag('h1').mouse_out()

``click``
---------

.. highlight:: python

Clicks on the element. Example:

::

    browser.find_by_tag('h1').click()

``double_click``
----------------

.. highlight:: python

Double-clicks on the element. Example:

::

    browser.find_by_tag('h1').double_click()

``right_click``
---------------

.. highlight:: python

Right-clicks on the element. Example:

::

    browser.find_by_tag('h1').right_click()

``drag_and_drop``
-----------------

Yes, you can drag an element and drop it to another element! The example below
drags the ``<h1>...</h1>`` element and drop it to a container element
(identified by a CSS class).

.. highlight:: python

::

    draggable = browser.find_by_tag('h1')
    target = browser.find_by_css('.container')
    draggable.drag_and_drop(target)
