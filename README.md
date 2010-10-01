splinter - Python acceptance testing for web applications 

## development

* Source hosted at [GitHub](http://github.com/cobrateam/splinter)
* Report issues on [GitHub Issues](http://github.com/cobrateam/splinter/issues)

Pull requests are very welcome! Make sure your patches are well tested.

### running the tests

if you are using a virtualenv, all you need is:

    make test

### community

channel #cobrateam on irc.freenode.net

## documentation

### Browser

For use splinter you need create a Browser instance:

    from splinter.browser import Browser
    browser = Browser()

### Navigating with Browser.visit

You can use the <tt>visit</tt> method to navigate to other pages:
    
    browser.visit('http://cobrateam.info')

The visit method only takes a single parameter for <tt>url</tt> will be visited, the request method is *always*
GET.

### Browser.title

You can get a title of a page visited using <tt>title</tt> attribute:

    browser.title
    
### Verifying page content with Browser.html

You can use the <tt>html</tt> attribute to get the html content for the page visited:

    browser.html
    
### Verifying page url with Browser.url

You can get <tt>url</tt> attribute to get url for the page visited:
    
    browser.url
    
### Finding elements

For finding elements you can use five methods, one for each selector type <tt>css_selector</tt>, <tt>id</tt>, <tt>tag</tt>, <tt>name</tt> or <tt>xpath</tt>:

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
    
For find link by id, tag, name or xpath you can use defaults find methods.
    
### Get element value

If you need get value for a element, you can use the <tt>value</tt> attribute:

    browser.find_by_css_selector('h1').value
    
or
    element = browser.find_by_css_selector('h1')
    element.value
    
### Interacting with forms

    browser.fill_in('query', 'my name')
    browser.choose("some-radio")
    browser.check("some-check")
    browser.uncheck("some-check")
    
### Verifying if element is visible or invisible

You can use <tt>visible</tt> attribute for verify if element is visible or invisible. If 
element is visible the <tt>visible</tt> attribute returns <tt>True</tt>, else returns <tt>False</tt>.

    browser.find_by_css_selector('h1').visible