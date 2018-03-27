.. Copyright 2014 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Using HTTP proxies
    :keywords: splinter, python, tutorial, documentation, proxy

++++++++++++++++++++++++++++++++++++++++++++
Using HTTP Proxies
++++++++++++++++++++++++++++++++++++++++++++

Unauthenticated proxies are simple, you need only configure
the browser with the hostname and port.

Authenticated proxies are rather more complicated, (see
`RFC2617 <http://www.ietf.org/rfc/rfc2617.txt>`_)

Using an unauthenticated HTTP proxy with Firefox
------------------------------------------------

::

    profile = {
        'network.proxy.http': YOUR_PROXY_SERVER_HOST,
        'network.proxy.http_port': YOUR_PROXY_SERVER_PORT,
        'network.proxy.ssl': YOUR_PROXY_SERVER_HOST,
        'network.proxy.ssl_port': YOUR_PROXY_SERVER_PORT,
        'network.proxy.type': 1
    }
    self.browser = Browser(self.browser_type, profile_preferences=profile)

Authenticated HTTP proxy with Firefox
-------------------------------------

If you have access to the browser window, then the same technique will
work for an authenticated proxy, but you will have to type the username
and password in manually.

If this is not possible, for example on a remote CI server, then it is
not currently clear how to do this. This document will be updated when
more information is known. If you can help, please follow up on
`https://github.com/cobrateam/splinter/issues/359 <https://github.com/cobrateam/splinter/issues/359>`_.

