from django.conf.urls import include, url
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import admin
from django.contrib.auth.decorators import login_required
import six

from tests.fake_webapp import (
    EXAMPLE_HTML,
    EXAMPLE_IFRAME_HTML,
    EXAMPLE_ALERT_HTML,
    EXAMPLE_TYPE_HTML,
    EXAMPLE_NO_BODY_HTML,
    EXAMPLE_POPUP_HTML,
    EXAMPLE_REDIRECT_LOCATION_HTML
)


admin.autodiscover()


def index(request):
    return HttpResponse(EXAMPLE_HTML)


def iframed(request):
    return HttpResponse(EXAMPLE_IFRAME_HTML)


def alertd(request):
    return HttpResponse(EXAMPLE_ALERT_HTML)


def type(request):
    return HttpResponse(EXAMPLE_TYPE_HTML)


def no_body(request):
    return HttpResponse(EXAMPLE_NO_BODY_HTML)


def get_name(request):
    return HttpResponse("My name is: Master Splinter")


def get_user_agent(request):
    return HttpResponse(request.META['User-Agent'])


def request_headers(request):
    body = '\n'.join('%s: %s' % (key, value) for key, value in six.iteritems(request.META))
    return HttpResponse(body)


def upload_file(request):
    if request.method == 'POST':
        f = request.FILES['file']
        buffer = []
        buffer.append("Content-type: %s" % f.content_type)
        buffer.append("File content: %s" % f.read())

        return HttpResponse('|'.join(buffer))


def foo(request):
    return HttpResponse("BAR!")


def query_string(request):
    if request.query_string == "model":
        return HttpResponse("query string is valid")
    else:
        raise Exception('500')


def popup(request):
    return HttpResponse(EXAMPLE_POPUP_HTML)


@login_required
def auth_required(request):
    return HttpResponse("Success!")


def redirected(request):
    location = '{}?{}'.format(reverse('redirect_location'), 'come=get&some=true')
    return redirect(location)


def redirect_location(request):
    return HttpResponse(EXAMPLE_REDIRECT_LOCATION_HTML)


urlpatterns = [
    url(r'^$', index),
    url(r'^iframe$', iframed),
    url(r'^alert$', alertd),
    url(r'^type$', type),
    url(r'^no_body$', no_body),
    url(r'^name$', get_name),
    url(r'^useragent$', get_user_agent),
    url(r'^headers$', request_headers),
    url(r'^upload$', upload_file),
    url(r'^foo$', foo),
    url(r'^query$', query_string),
    url(r'^popup$', popup),
    url(r'^authenticate$', auth_required),
    url(r'^redirected', redirected),
    url(r'^redirect-location', redirect_location, name='redirect_location'),
    url(r'^admin/', include(admin.site.urls)),
]
