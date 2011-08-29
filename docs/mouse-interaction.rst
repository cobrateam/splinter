.. meta::
    :description: Mouse interatcion.
    :keywords: splinter, python, tutorial, documentation, mouse interaction, mouseover, mouseout, doube click 

+++++++++++++++++
Mouse interaction
+++++++++++++++++

Mouse interaction currently works only on Chrome driver.

mouseover
---------

.. highlight:: python

::

    browser.find_by_css('h1').mouseover()

mouseout
--------

.. highlight:: python

::

    browser.find_by_css('h1').mouseout()

doube click
-----------

.. highlight:: python

::

    browser.find_by_css('h1').double_click()
