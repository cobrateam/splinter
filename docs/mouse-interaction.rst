.. meta::
    :description: Mouse interatcion.
    :keywords: splinter, python, tutorial, documentation, mouse interaction, mouseover, mouseout, doube click, mouse events

++++++++++++++++++
Mouse interactions
++++++++++++++++++

    **Note:** Mouse interaction currently works only on Chrome driver.

splinter provide some methods for mouse interactions with elements in the page. This feature is useful to
test if an element appears on mouse over, and disappears on mouse out (e.g.: submitems of a menu).

It's also possible to send a click, double click or right click to the element.

Here is a simple example: imagine you have a `jQuery <http://jquery.com>`_ event for mouse over and out:

.. highlight:: js

::

    $('.menu-links').mouseover(function(){
        $(this).find('.subitem').show();
    });

    $('.menu-links').mouseout(function(){
        $(this).find('.subitem').hide();
    });

You can use splinter to fire the event programatically:

.. highlight:: python

::

    browser.find_by_css('.menu-links').mouse_over()
    # check if the subitem is visible
    browser.find_by_css('.menu-links').mouse_out()


mouse over
----------

.. highlight:: python

::

    browser.find_by_css('h1').mouseo_ver()

mouse out
---------

.. highlight:: python

::

    browser.find_by_css('h1').mouse_out()

click
-----

.. highlight:: python

::

    browser.find_by_css('h1').click()

double click
------------

.. highlight:: python

::

    browser.find_by_css('h1').double_click()

right click
-----------

.. highlight:: python

::

    browser.find_by_css('h1').right_click()

drag and drop
-------------

You can drag an element and drop it to another element.

The code below drags the ``<h1></h1>`` element and drop it to a container element (identified by
a CSS class).

.. highlight:: python

::

    target_element = browser.find_by_css('.container')
    browser.find_by_css('h1').drag_and_drop(target_element)
