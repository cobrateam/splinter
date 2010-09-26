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

### Navigating

You can use the <tt>visit</tt> method to navigate to other pages:
    
    from splinter.browser import Browser
    browser.visit('http://cobrateam.info')

The visit method only takes a single parameter for <tt>url</tt> will be visited, the request method is *always*
GET.