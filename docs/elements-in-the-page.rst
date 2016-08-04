.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Dealing with elements in the page.
    :keywords: splinter, python, tutorial, documentation, forms, click links, get value

+++++++++++++++++++++++++++++++++++++
Interacting with elements in the page
+++++++++++++++++++++++++++++++++++++

Get value of an element
-----------------------

In order to retrieve an element's value, use the ``value`` property:

.. highlight:: python

::

    browser.find_by_css('h1').first.value

or

.. highlight:: python

::

    element = browser.find_by_css('h1').first
    element.value


Clicking links
--------------

You can click in links. To click in links by href, partial href, text or partial text you can use this.
IMPORTANT: These methods return the first element always.

.. highlight:: python

::

    browser.click_link_by_href('http://www.the_site.com/my_link')

or

.. highlight:: python

::

    browser.click_link_by_partial_href('my_link')

or

.. highlight:: python

::

    browser.click_link_by_text('my link')

or

.. highlight:: python

::

    browser.click_link_by_partial_text('part of link text')

or

.. highlight:: python

::

    browser.click_link_by_id('link_id')


Clicking buttons
----------------

You can click in buttons. Splinter follows any redirects, and submits forms associated with buttons.

.. highlight:: python

::

    browser.find_by_name('send').first.click()

or

.. highlight:: python

::

    browser.find_link_by_text('my link').first.click()


Interacting with forms
----------------------

.. highlight:: python

::

    browser.fill('query', 'my name')
    browser.attach_file('file', '/path/to/file/somefile.jpg')
    browser.choose('some-radio', 'radio-value')
    browser.check('some-check')
    browser.uncheck('some-check')
    browser.select('uf', 'rj')

To trigger JavaScript events, like KeyDown or KeyUp, you can use the `type` method.

.. highlight:: python

::

    browser.type('type', 'typing text')

If you pass the argument `slowly=True` to the `type` method you can interact with the
page on every key pressed. Useful for testing field's autocompletion (the browser
will wait until next iteration to type the subsequent key).

.. highlight:: python

::

    for key in browser.type('type', 'typing slowly', slowly=True):
        pass # make some assertion here with the key object :)

You can also use ``type`` and ``fill`` methods in an element:

.. highlight:: python

::

    browser.find_by_name('name').type('Steve Jobs', slowly=True)
    browser.find_by_css('.city').fill('San Francisco')


Verifying if element is visible or invisible
--------------------------------------------

To check if an element is visible or invisible, use the ``visible`` property. For instance:

.. highlight:: python

::

    browser.find_by_css('h1').first.visible

will be True if the element is visible, or False if it is invisible.


Verifying if element has a className
------------------------------------

To check if an element has a className, use the ``has_class`` method. For instance:

.. highlight:: python

::

    browser.find_by_css('.content').first.has_class('content')


Interacting with elements through a ElementList object
------------------------------------------------------

Don't you like to always use ``first`` when selecting an element for clicking, for example:

.. highlight:: python

::

    browser.find_by_css('a.my-website').first.click()

You can invoke any ``Element`` method on ``ElementList`` and it will be proxied to the **first** element of the list. So the two lines below are equivalent:

.. highlight:: python

::

    assert browser.find_by_css('a.banner').first.visible
    assert browser.find_by_css('a.banner').visible

