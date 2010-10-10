splinter - Python acceptance testing for web applications 

## development

* Source hosted at [GitHub](http://github.com/cobrateam/splinter)
* Report issues on [GitHub Issues](http://github.com/cobrateam/splinter/issues)

Pull requests are very welcome! Make sure your patches are well tested.

### running the tests

if you are using a virtualenv, all you need is:

    $ make test

### community

\#cobrateam channel on irc.freenode.net

## documentation

### Browser

To use splinter you need create a Browser instance:

    from splinter.browser import Browser
    browser = Browser()

### Navigating with Browser.visit

You can use the <tt>visit</tt> method to navigate to other pages:
    
    browser.visit('http://cobrateam.info')

The <tt>visit</tt> method takes only a single parameter - the <tt>url</tt> to be visited.

### Browser.title

You can get the title of the visited page using the <tt>title</tt> attribute:

    browser.title
    
### Verifying page content with Browser.html

You can use the <tt>html</tt> attribute to get the html content of the visited page:

    browser.html
    
### Verifying page url with Browser.url

The visited page's url can be accessed by the <tt>url</tt> attribute:
    
    browser.url
    
### Finding elements

For finding elements you can use five methods, one for each selector type <tt>css_selector</tt>, <tt>xpath</tt>, <tt>tag</tt>, <tt>name</tt>, <tt>id</tt>:

    browser.find_by_css_selector('h1')
    browser.find_by_xpath('//h1')
    browser.find_by_tag('h1')
    browser.find_by_name('name')
    browser.find_by_id('firstheader')
    
### Finding links

For finding link elements you can use <tt>find_link_by_text</tt> or <tt>find_link_by_href</tt>:

    browser.find_link_by_text('Link for Example.com')
    
or

    browser.find_link_by_href('http://example.com')

For finding links by id, tag, name or xpath you should use other find methods (<tt>find_by_css_selector</tt>, <tt>find_by_xpath</tt>, <tt>find_by_tag</tt>, <tt>find_by_name</tt> and <tt>find_by_id</tt>).


### Get element value

In order to retrieve an element's value, use the <tt>value</tt> property:

    browser.find_by_css_selector('h1').value

or

    element = browser.find_by_css_selector('h1')
    element.value
    
### Interacting with forms

    browser.fill_in('query', 'my name')
    browser.choose('some-radio')
    browser.check('some-check')
    browser.uncheck('some-check')
    
### Verifying if element is visible or invisible

To check if an element is visible or invisible, use the <tt>visible</tt> property. For instance:

    browser.find_by_css_selector('h1').visible

will be True if the element is visible, or False if it is invisible.

### Executing javascript

You can easily execute JavaScript, in drivers which support it:

    browser.execute_script("$('body').empty()")
    
You can return the result of the script:

    browser.evaluate_script("4+4") == 8
