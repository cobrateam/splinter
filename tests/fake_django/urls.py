from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import re_path, reverse

from tests.fake_webapp import (
    EXAMPLE_HTML,
    EXAMPLE_IFRAME_HTML,
    EXAMPLE_ALERT_HTML,
    EXAMPLE_TYPE_HTML,
    EXAMPLE_NO_BODY_HTML,
    EXAMPLE_POPUP_HTML,
    EXAMPLE_REDIRECT_LOCATION_HTML,
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
    return HttpResponse(request.META["User-Agent"])


def post_form(request):
    items = "\n".join("{}: {}".format(*item) for item in request.POST.items())
    body = "<html><body>{}</body></html>".format(items)
    return HttpResponse(body)


def request_headers(request):
    body = "\n".join(
        "%s: %s" % (key, value) for key, value in request.META.items()
    )
    return HttpResponse(body)


def upload_file(request):
    if request.method == "POST":
        f = request.FILES["file"]
        buffer = [
            "Content-type: {}".format(f.content_type),
            "File content: {}".format(f.read()),
        ]
        return HttpResponse("|".join(buffer))


def foo(request):
    return HttpResponse("BAR!")


def query_string(request):
    if request.query_string == "model":
        return HttpResponse("query string is valid")
    else:
        raise Exception("500")


def popup(request):
    return HttpResponse(EXAMPLE_POPUP_HTML)


@login_required
def auth_required(request):
    return HttpResponse("Success!")


def redirected(request):
    location = "{}?{}".format(reverse("redirect_location"), "come=get&some=true")
    return redirect(location)


def redirect_location(request):
    return HttpResponse(EXAMPLE_REDIRECT_LOCATION_HTML)


urlpatterns = [
    re_path(r"^$", index),
    re_path(r"^iframe$", iframed),
    re_path(r"^alert$", alertd),
    re_path(r"^type$", type),
    re_path(r"^no_body$", no_body),
    re_path(r"^name$", get_name),
    re_path(r"^useragent$", get_user_agent),
    re_path(r"^headers$", request_headers),
    re_path(r"^upload$", upload_file),
    re_path(r"^foo$", foo),
    re_path(r"^query$", query_string),
    re_path(r"^popup$", popup),
    re_path(r"^authenticate$", auth_required),
    re_path(r"^redirected", redirected),
    re_path(r"^post", post_form),
    re_path(r"^redirect-location", redirect_location, name="redirect_location"),
]

urlpatterns.append(url(r"^admin/", admin.site.urls))
