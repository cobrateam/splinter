+++++++++++++++++
Why use Splinter?
+++++++++++++++++

Splinter is an abstraction layer on top of existing browser automation tools
such as `Selenium`_ and `zope.testbrowser`_. It has a :doc:`high-level API
</api/index>` that makes it easy to write automated tests of web applications.

For example, to fill out a form field with Splinter::

    browser.fill('username', 'janedoe')

In Selenium, the equivalent code would be::

    elem = browser.find_element.by_name('username')
    elem.send_keys('janedoe')

Because Splinter is an abstraction layer, it supports multiple web automation
backends. With Splinter, you can use the same test code to do browser-based
testing with Selenium as the backend and "headless" testing (no GUI) with
zope.testbrowser as the backend.

Splinter has drivers for browser-based testing on:

* :doc:`Chrome </drivers/chrome>`
* :doc:`Firefox </drivers/firefox>`
* :doc:`Browsers on remote machines </drivers/remote>`

For headless testing, Splinter has drivers for:

* :doc:`zope.testbrowser </drivers/zope.testbrowser>`
* :doc:`Django client </drivers/django>`
* :doc:`Flask client </drivers/flask>`


.. _Selenium: http://seleniumhq.org
.. _zope.testbrowser: https://launchpad.net/zope.testbrowser
