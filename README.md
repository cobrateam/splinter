splinter is based in [capybara](http://github.com/jnicklas/capybara)



## running the tests

if you are using a virtualenv, all you need is:

    make test

## community

channel #cobrateam on irc.freenode.net

## contributing to splinter

1. fork and clone the project
2. hack
3. commit and push
4. send a pull request

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
    
### Browser.html

You can use the <tt>html</tt> attribute to get the html content for the page visited:

    browser.html