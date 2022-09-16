+++++++++++++++++
Why Use Splinter?
+++++++++++++++++


Splinter is used to write web browser automation scripts.

The project has two primary goals:

* Provide a :doc:`common, high-level API </api/index>` on top of existing
  browser automation tools such as `Selenium`_. The API is an abstraction layer
  that is human-friendly and designed for easy, efficient scripting.

* Provide built-in functionality to handle common pain points with browser automation.


Example
~~~~~~~

The following code will type text into an input element:


Written in Splinter:

.. code-block:: python

    from splinter import Browser

    browser = Browser('chrome')
    browser.visit('http://cowabunga.tubular.awesome')

    element = browser.find_by_css('.username')
    element.fill('Michaelangelo')


Written in Selenium:

.. code-block:: python

    from selenium import webdriver
    from selenium.webdriver.common.by import By

    driver = webdriver.Chrome()
    driver.get('http://cowabunga.tubular.awesome')

    element = driver.find_elements(by=By.CSS_SELECTOR, value='.username')
    element.send_keys('Michaelangelo')


Splinter's API provides a clean interface, but there's more going on here:

.. code-block:: python
    :emphasize-lines: 6

    from splinter import Browser

    browser = Browser('chrome')
    browser.visit('http://cowabunga.tubular.awesome')

    element = browser.find_by_css('.username')
    element.fill('Michaelangelo')


Under the hood, Splinter will wait for an element to be in a safe state for interaction.
This prevents common errors where elements may be found before the web application is ready.

Splinter supports multiple web automation back-ends. You can use the same code
for web browser testing with Selenium as the back-end and
"headless" testing (no GUI) with zope.testbrowser as the backend.

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
