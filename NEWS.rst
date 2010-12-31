+++++++++++
splinter news
+++++++++++

what's new in splinter 0.0.2?
================================

Features
-----------------

- Issue #11: improve find's methods for return all/first/last elements

Now the finder methods returns a QueryElements object that contains a list of all found elements.

Have four ways to get elements in a QueryElements object:

.all() - for get all elements

::

	browser.find_by_name('name').all()
	
.first() - for get first element

::

	browser.find_by_name('name').first()

.last() - for get last element

::

	browser.find_by_name('name').last()

using index

::

	browser.find_by_name('name')[1]
	
A web page should be only one id per page. Then find_by_id().all() method return always a list with one element.

what's new in splinter 0.0.1?
================================

Features
-----------------

- suport to firefox selenium 2 driver
- suport to zope test browser
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