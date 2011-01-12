+++++++++++++
splinter news
+++++++++++++

what's new in splinter 0.0.2?
================================

Features
-----------------

- support to google chrome selenium 2 driver

Backward incompatible changes
-----------------------------

- issue #24 remove save_and_open_page method from splinter api. This feature is out of splinter's scope, hence should be implemented as an external package.


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