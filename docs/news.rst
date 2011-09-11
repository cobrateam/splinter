.. meta::
    :description: New splinter features on earlier versions.
    :keywords: splinter, python, news, documentation, tutorial, web application

+++++++++++++
splinter news
+++++++++++++

whats's new in splinter 0.4?
============================

Features
--------

- support for double click, right click, drag and drop and other :doc:`mouse interactions </mouse-interaction>`
  (only :doc:`Chrome </drivers/chrome>` driver)
- support for Python 2.5

Documentation improvements
--------------------------

- improved :doc:`API docs </api/index>`
- added docs for ``is_text_present`` method
- added API docs for ``is_element_present_by_*`` methods
- added docs for :doc:`mouse interactions </mouse-interaction>`

Deprecations
------------

- simplified name of Selenium drivers, they're just ``chrome`` and ``firefox`` now (instead
  of ``webdriver.chrome`` and ``webdriver.firefox``). The older names were deprecated.
- changed name of ``mouseover`` and ``mouseout`` methods to ``mouse_over`` and ``mouse_out``

IMPORTANT
---------

The following deprecated methods will be **removed** in the next splinter release (0.5) from Browser classes:

- fill_in
- find_by_css_selector
- is_element_present_by_css_selector
- is_element_not_present_by_css_selector

what's new in splinter 0.3?
===========================

Features
--------

- support for browser extensions on :doc:`Firefox driver </drivers/firefox>`
- support for Firefox profiles on :doc:`Firefox driver </drivers/firefox>`
- support for mouse over and mouse out on :doc:`Chrome driver </drivers/chrome>`
- support for finding and clicking links by partial :meth:`text <splinter.driver.DriverAPI.click_link_by_partial_text>`
  and :meth:`href <splinter.driver.DriverAPI.click_link_by_partial_href>`
- support for :meth:`finding by value <splinter.driver.DriverAPI.find_by_value>`

Documentation improvements
--------------------------

- complete :doc:`API reference </api/index>`
- instructions on :doc:`new drivers creation </contribute/writing-new-drivers>`

Backward incompatible changes
-----------------------------

- changes on :doc:`cookies manipulation </cookies>`. Affects only who used :meth:`cookies.delete <splinter.cookie_manager.CookieManagerAPI.delete>`
  passing the ``cookie`` keyword.

Before version **0.3**:

.. highlight:: python

::

    >>> driver.cookies.delete(cookie='whatever')

Now:

.. highlight:: python

::

    >>> driver.cookies.delete('whatever')

Bugfixes
--------

- Fixed cookies behavior on Chrome driver (it was impossible to delete one cookie, Chrome was always deleting all cookies)

what's new in splinter 0.2?
===========================

Features
--------

- :doc:`cookies manipulation </cookies>`
- find elements within an element
- improvements in `ElementList`

Backward incompatible changes
-----------------------------

- you should update your selenium to 2.1.0 version and your chrome driver. See more in :doc:`suport to new chrome driver </drivers/chrome>`

what's new in splinter 0.1.1?
=============================

- compability with Firefox 5

what's new in splinter 0.1?
===========================

Features
--------

- capability to handle HTTP errors (using an exception) in Selenium drivers (Firefox and Chrome)
- capability to work with HTTP status code in Selenium drivers (Firefox and Chrome)
- browsing history (``back`` and ``forward`` methods in ``Browser`` class)
- improvements in documentation

Bugfixes
--------

- fixed Chrome driver instability
- fixed ``Browser.choose`` behaviour
- fixed WebDriver silenting routine

Backward incompatible changes
-----------------------------

- you should update your selenium to 2.0rc2 version

what's new in splinter 0.0.3?
=============================

Features
--------

- now splinter use selenium 2.0b3 for firefox and chrome driver
- zope.testbrowser.browser dependency is not required
- new method for reload a page
- find_by_css_selector is now deprecated, use find_by_css instead
- deprecated methods now throw "DeprecationWarning"
- methods for verify if element or text is present
- find_by methods wait for element
- added support for iframes and alerts
- added more specific exception messages for not found elements

Backward incompatible changes
-----------------------------

- you should update your selenium to 2.0b3 version

what's new in splinter 0.0.2?
=============================

Features
--------

- fill instead of fill_in to fill inputs
- support to google chrome selenium 2 driver
- form interactions now support select
- issue #11: improve find's methods to return all/first/last elements

now finder methods (find_by_name, find_by_css_selector, find_by_tag, find_by_id, find_by_xpath) returns a ElementList object that contains a list of all found elements:

::

	browser.find_by_name('name')

.first - to find first element

::

	browser.find_by_name('name').first

.last - to find last element

::

	browser.find_by_name('name').last

And additionally, using index

::

	browser.find_by_name('name')[1]

An id should be unique in a web page, so find_by_id() method always returns a list with a single element.

Backward incompatible changes
-----------------------------

- issue #24 remove save_and_open_page method from splinter api. This feature is out of splinter's scope, hence should be implemented as an external package.
- now finder methods (find_by_name, find_by_css_selector, find_by_tag, find_by_id, find_by_xpath) returns a list with elements, to get the first element founded use `first` attribute

::

	browser.find_by_name('name').first

what's new in splinter 0.0.1?
================================

Features
-----------------

- support to firefox selenium 2 driver
- support to zope test browser
- navigating with Browser.visit
- get the title of the visited page
- get the html content of the visited page
- visited page's url can be accessed by the url attribute
- finding first element by tag, xpath, css selector, name and id
- find first link by xpath or text
- interacting with forms: text input, file, radio and check button
- verifying if element is visible or invisible
- executing and evaluating javascript
- debug with save and open page
