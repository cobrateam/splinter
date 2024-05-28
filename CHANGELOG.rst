.. meta::
    :description: Splinter Changelog
    :keywords: changelog

[0.21.0]
========

Changed
-------

* `Safari` is now supported as a browser for Selenium Remote

[0.20.1]
========

Fixed
-----

* Fix the default value for User-Agent

[0.20.0]
========

Changed
-------

* Selenium 3 is no longer supported
* Added support for Python 3.11 and 3.12, dropped support for Python 3.7

Fixed
-----

* CookieManager.delete() no longer deletes all cookies when no arguments are given

[0.19.0]
========

Added
-----

* The methods WebDriverElement.is_visible() and WebDriverElement.is_not_visible() are now available as a replacement for WebDriver.is_element_not_visible_by_css and WebDriver.is_element_visible_by_css.
  See https://splinter.readthedocs.io/en/latest/matchers.html#checking-the-visibility-of-elements for more information.

Changed
-------

* When CookieManager.delete() is called with no arguments then all cookies are deleted. This behaviour has been deprecated. CookieManager.delete_all() should be used instead.
* The message for the error raised when a driver's class is not found has been improved.

Fixed
-----

* FlaskDriver.attach_file() has been fixed.
* urllib3 is now always installed, regardless of driver used.

[0.18.1]
========

Changed
-------

* Set Firefox preferences through options instead of FirefoxProfile

Fixed
-----

* Use dedicated logger in browser.py to avoid *clobbering* other Python logging
* Removed required selenium import for error handling, making it possible to use splinter without installing selenium (as long as a selenium driver isn't used)

[0.18.0]
========

Added
-----

* WebDriverElement() now implements the `shadow_root` property. This returns a ShadowRootElement() object to interact with the shadow root of an element.
* Failed driver imports are logged at the debug level instead of silently ignored
* `browser.html_snapshot()` now takes the optional `unique_file` argument. Setting this to False will disable the addition of random characters to the filename.

Changed
-------

* repr(ElementList()) now returns the repr of the internal container.
* Driver.find_link_by_<x> methods have been removed. Use Driver.links.find_by_<x>.
* Screenshot taken by WebDriverElement.screenshot() now implements Selenium's element screenshot instead of cropping a full page screenshot.
* Flask/Django's back/forward methods more accurately store browsing history
* Official Python 3.6 support has been removed

Fixed
-----

* 0.17.0 would report as 0.16.0. 0.18.0 reports correctly.
* When using Firefox, extensions can now be installed

[0.17.0]
========

* Added parameter to DriverAPI.screenshot and ElementAPI.screenshot to indicate if unique filename should be ensured (https://github.com/cobrateam/splinter/pull/949)
* Added Selenium 4 support

Backward incompatible changes
-----------------------------

* Removed python 2.7 support (https://github.com/cobrateam/splinter/pull/952)
* Selenium 3 is no longer installed by default. To install Selenium 3, use the `selenium3` extra argument

.. code-block:: bash

    python -m pip install splinter[selenium3]

[0.16.0]
========

* Pin Selenium < 4.0 (https://github.com/cobrateam/splinter/pull/930)
* Add support for Microsoft Edge (https://github.com/cobrateam/splinter/pull/912)
* Accept extra arguments for cookies (https://github.com/cobrateam/splinter/pull/895)
* Fix lxmldriver url join when form action is empty (https://github.com/cobrateam/splinter/pull/900)
* Use io.open() to fix encoding issues on some platforms (https://github.com/cobrateam/splinter/pull/904)
* allow passing options to Firefox webdriver (https://github.com/cobrateam/splinter/pull/892)

Backward incompatible changes
-----------------------------
* Remove sending a list of cookie dicts to CookieManager.add() (https://github.com/cobrateam/splinter/pull/799)

[0.15.0]
========

* Add more input types to Webdriver clear() (https://github.com/cobrateam/splinter/pull/780)
* Standardize init of CookieManager (https://github.com/cobrateam/splinter/pull/795)
* Add delete_all method to CookieManager (https://github.com/cobrateam/splinter/pull/797)
* Warn user when cookies list is used (https://github.com/cobrateam/splinter/pull/801)
* Added retry_count to get_driver (https://github.com/cobrateam/splinter/pull/754)
* Fix full screen screenshot (https://github.com/cobrateam/splinter/pull/810)
* Add flag to ignore missing fields in fill_form (https://github.com/cobrateam/splinter/pull/821)
* Opening a link in a new tab (https://github.com/cobrateam/splinter/pull/800)

[0.14.0]
========

* Add FindLinks api to non-webdrivers (https://github.com/cobrateam/splinter/pull/762)
* Add support for zope in python3 (https://github.com/cobrateam/splinter/pull/771)
* Fix WebDriverElement.screenshot when parent is a WebDriverElement (https://github.com/cobrateam/splinter/pull/769)
* Improve firefox headless support (https://github.com/cobrateam/splinter/pull/768)
* Fix mouse out on elements in the left corner of the viewport (https://github.com/cobrateam/splinter/pull/766)
* Fix fullscreen argument for firefox (https://github.com/cobrateam/splinter/pull/765)
* Fix unexpected keyword argument 'original_find' (https://github.com/cobrateam/splinter/pull/758)
* Fix incorrect error thrown when missing chrome/geckodriver (https://github.com/cobrateam/splinter/pull/749)
* Make find_by_value works with button elements (https://github.com/cobrateam/splinter/pull/746)

[0.13.0]
========

* Patch Remote WebDriver to add retry attempts (https://github.com/cobrateam/splinter/pull/742)
* Add driver attribute to WebDriverElement. This fixes an issue where mouse interaction fails on nested elements (https://github.com/cobrateam/splinter/pull/740)
* Fix WebDriverElement.select and .select_by_text to search only inside the parent element (https://github.com/cobrateam/splinter/pull/729)
* find_by with 0 second wait_time only checks once (https://github.com/cobrateam/splinter/pull/739)
* Fix FlaskClient redirects (https://github.com/cobrateam/splinter/pull/721)

[0.12.0]
========

* `find_by_text` now handle strings with quotation marks (https://github.com/cobrateam/splinter/issues/457)
* `find_link_by` methods are now chainable (https://github.com/cobrateam/splinter/pull/699)
* `ElementList.__getattr__()` no longer hide ElementNotFound (https://github.com/cobrateam/splinter/pull/707)
* Firefox headless mode now handle custom firefox_binary option (https://github.com/cobrateam/splinter/pull/714)
* Firefox driver now respects headless option in subsequent calls (https://github.com/cobrateam/splinter/pull/715)
* `Browser.get_alert()` returns None if no alert exists (https://github.com/cobrateam/splinter/issues/387)
* Retry WebElement.click if Exception is thrown (https://github.com/cobrateam/splinter/pull/725)
* `find_by` methods in WebDriverElement now uses retry mechanism (https://github.com/cobrateam/splinter/pull/727)
* `is_not_present/visible` returns True immediately after not finding anything (https://github.com/cobrateam/splinter/pull/732)
* Accept all valid arguments for Remote WebDriver (https://github.com/cobrateam/splinter/pull/734)
* Allow ActionChains when using Remote WebDriver (https://github.com/cobrateam/splinter/pull/738)

[0.11.0]
========

* Browser.get_alert() returns Alert instead of a wrapper object
* Add `browser.html_snapshot` method
* Allow browser.get_iframe() to accept a web element
* Fix mouse_out method
* ElementList is no longer a subclass of list
* Browser.get_alert() now waits for alert to present
* Use 'switch_to.alert' instead of deprecated 'switch_to_alert'

[0.10.0]
========

* Scroll to elements before to execute action chains ()
* Using `options` instead `firefox_options` to avoid warnings (https://github.com/cobrateam/splinter/pull/634)
* Add support for `*args` parameter in `execute_script` (https://github.com/cobrateam/splinter/issues/436)
* Implement `__ne__` in `StatusCode` (https://github.com/cobrateam/splinter/issues/460)
* Using the new syntax `switch_to_alert` instead `switch_to.alert` to avoid webdriver warnings.
* `CookieManager. __eq__` returns a bool value (https://github.com/cobrateam/splinter/issues/308<Paste>)
* Fix find_by_text to be used inside a chain (https://github.com/cobrateam/splinter/issues/6281)
* Add support for selenium 3.141.0

[0.9.0]
=======

* `phantomjs` support was removed (https://github.com/cobrateam/splinter/issues/592)
* add options argument for chrome driver (https://github.com/cobrateam/splinter/pull/345)
* (bugfix) avoid element.find_by_text searches whole dom (https://github.com/cobrateam/splinter/issues/612)
* add support for zope.testbrowser 5+
* handle webdriver StaleElementReferenceException (https://github.com/cobrateam/splinter/issues/541)
* add support for Flask 1+
* add support for selenium 3.14.0
* update lxml to 4.2.4
* update cssselect to 1.0.3

[0.8.0]
=======

* add support for Firefox incognito mode (https://github.com/cobrateam/splinter/pull/578)
* allow return value for `execute_script` to be returned (https://github.com/cobrateam/splinter/pull/585)
* `chrome_options` parameter renamed to `options` (https://github.com/cobrateam/splinter/pull/590)
* removed deprecated `mouseover` method
* raises `NotImplementedError` on `status_code` in drivers based on webdriver
* `phantomjs` is deprecated (this driver will be removed in 0.9.0)

[0.7.7]
=======

* `fill_form` more robust by requiring form ID
* support firefox `headless mode`
* handle exceptions when calling quit on webdriver

[0.7.6]
=======

* fix `fill_form` for `select` element.
* support chrome headless mode

[0.7.5]
=======

* Timeout settings for Firefox driver
* Remove default icognito mode in Chrome driver
* Make input a contro element in `django`, `flask` and `zope.testbrowser`

[0.7.4]
=======

* support Selenium 2.53.6
* find_by_text support quotes (`#420 <https://github.com/cobrateam/splinter/pull/420>`_).
* Selenium capabilities for Firefox driver
  (`#417 <https://github.com/cobrateam/splinter/pull/417>`_).
* multi-select support for Django and Flask
  (`#443 <https://github.com/cobrateam/splinter/pull/443>`_).
* custom headers support to Flask
  (`#444 <https://github.com/cobrateam/splinter/pull/444>`_).
* add `in` operation for cookies
  (`#445 <https://github.com/cobrateam/splinter/pull/445>`_).
* Support for `is_element_present_by_*` in non-javascript drivers
  (`#463 <https://github.com/cobrateam/splinter/pull/463>`_).
* incognito mode for Google Chrome
  (`#465 <https://github.com/cobrateam/splinter/pull/465>`_).
* support for clearing text field types
  (`#479 <https://github.com/cobrateam/splinter/pull/479>`_).
* allow to pass a chrome Options instance to Browser
  (`#494 <https://github.com/cobrateam/splinter/pull/494>`_).
* new click_link_by_id method
  (`#498 <https://github.com/cobrateam/splinter/pull/498>`_).

Backward incompatible changes
-----------------------------

* RequestHandler is removed and the `status` use lazy evaluation.

[0.7.3]
=======

* support selenium 2.47.1
* add `select_by_text` method
* add `find_by_text`, `is_element_present_by_text`, `is_element_not_present_by_text`
* improved support to python 3
* cookie support for remote webdriver
* get `status_code` by lazy evaluation. It should minimize the proxy and duplicated requests problems

django client
-------------

* improved `is_text_present` performance. djangoclient doesn't have to wait for load
* support django 1.7 and 1.8
* fixed several bugs with python3 compatibility
* added default extra headers: `SERVER_PORT`, `SERVER_NAME` and `User-Agent`
* support custom headers

[0.7.2]
=======

* fix Python 3 compatibility, improving enconding/decoding in `browser.title` and `browser.html` - `#380 <https://github.com/cobrateam/splinter/pull/380>`_

[0.7.1]
=======

* support Selenium 2.45.0.
* Django Client supports `**kwargs` parameters on constructor.
* Django Client handle redirects.
* ZopeTestBrowser has the `ignore_robots` parameter.

[0.7.0]
=======

Features
--------

* Support for mouse_over, mouse_out in Firefox driver.
* New flask test client driver.
* Better support for browser windows.
* Support for custom headers in PhantomJS driver.
* Added webdriver fullscreen support.
* Added a way to wait until element is visible.

Bugfix
------

* Support encoding in django client and zopetestbrowser drivers.
* Browser.cookies.all() are more consistent and added a verbose mode.

[0.6.0]
=======

Features
--------

* support for django test client.

[0.5.5]
=======

Improvements
------------

* Handle "internet explorer" as remote driver.
* implemented `get_screenshot_as_file`.
* `fill_form` now supports custom field types.
* More robust `find_link_by_partial_text`.
* support for selenium 2.39.0.
* support for zope.testbrowser 4.0.4.

[0.5.4]
=======

Improvement
-----------

* implemented `browser.cookies.all()` - #240.

Bugfix
------

* `browser.type()` works with textarea - #216.

[0.5.3]
=======

Improvement
-----------

* added kwargs to the Chrome driver constructor
* updated selenium to 2.33.0.

Bugfix
------

* fixed about:blank behaviour #233.

[0.5.2]
=======

Improvements
------------

* support password field.

[0.5.0]
=======

Features
--------

* support for phantomjs web driver.
* zopetestdriver support is_text_present.

Bugfix
------

* fixed an unicode issue with setup.py.

[0.4.10]
========

This version does not work with firefox 17.

Improvements
------------

* remove deprecated driver names
* update lxml version
* update selenium version to 2.29

Bugfix
------

* set user-agent for request_handler requests
* update zope.testbrowser documentation regarding dependencies (cssselect)
* fix URL checking in request_handler (support for HTTPS)

[0.4.9]
=======

This version does not works with firefox 17.

Features
--------

* support for selenium remote web driver.

Bugfix
------

* is_text_present and is_text_not_present works with html without body.
* fixed zopetestdriver attach_file behaviour.

[0.4.8]
=======

Features
--------

* html and outer_html property on Element
* profile_preferences option to Firefox driver
* Support for handling browser pop-up windows for Firefox/Chrome drivers.

[0.4.7]
=======

Features
--------

* has_class method on Element
* fix documentation

Bugfixes and improvements
-------------------------

* improving `find_by_css` method to use native methods from drivers

[0.4.4.1]
=========

Bugfixes
--------

* update selenium version, to work with latest Firefox version

[0.4.4]
=======

Features
--------

* Updated selenium to 2.17
* Method to change user-agent
* `dismiss` method in alert element


Bugfixes
--------

* request_handler now works with querystring

[0.4.3]
=======

Features
--------

* Updated selenium to 2.14

[0.4.2]
=======

Features
--------

* added new *browser* method *form_fill* to fill all form fields in one command

Bugfixes
--------

* fixed a bug in setup.py

[0.4.1]
=======

Features
--------

* Partial Windows support
* Internet Explorer driver
* Added ``type`` and ``fill`` methods to :doc:`ElementAPI </api/driver-and-element-api>`.
* Updated selenium to 2.13.1

[0.4.0]
=======

Features
--------

- support for double click, right click, drag and drop and other :doc:`mouse interactions </mouse-interaction>`
  (only :doc:`Chrome </drivers/chrome>` driver)
- support for Python 2.5

Documentation improvements
--------------------------

- improved API docs
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

[0.3.0]
=======

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

- complete API reference
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

[0.2.0]
=======

Features
--------

- :doc:`cookies manipulation </cookies>`
- find elements within an element
- improvements in `ElementList`

Backward incompatible changes
-----------------------------

- you should update your selenium to 2.1.0 version and your chrome driver. See more in :doc:`suport to new chrome driver </drivers/chrome>`

[0.1.1]
=======

- compatibility with Firefox 5

[0.1.0]
=======

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

[0.0.3]
=======

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

[0.0.2]
=======

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

[0.0.1]
=======

Features
--------

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
