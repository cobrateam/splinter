# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from flask import Flask, request, abort, Response
from os import path
from functools import wraps


this_folder = path.abspath(path.dirname(__file__))


def read_static(static_name):
    return open(path.join(this_folder, 'static', static_name)).read()

EXAMPLE_APP = "http://localhost:5000/"
EXAMPLE_HTML = read_static('index.html')
EXAMPLE_IFRAME_HTML = read_static('iframe.html')
EXAMPLE_ALERT_HTML = read_static('alert.html')
EXAMPLE_TYPE_HTML = read_static('type.html')
EXAMPLE_POPUP_HTML = read_static('popup.html')
EXAMPLE_NO_BODY_HTML = read_static('no-body.html')

# Functions for http basic auth. 
# Taken verbatim from http://flask.pocoo.org/snippets/8/
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

app = Flask(__name__)


@app.route('/')
def index():
    return EXAMPLE_HTML


@app.route('/iframe')
def iframed():
    return EXAMPLE_IFRAME_HTML


@app.route('/alert')
def alertd():
    return EXAMPLE_ALERT_HTML


@app.route('/type')
def type():
    return EXAMPLE_TYPE_HTML


@app.route('/no-body')
def no_body():
    return EXAMPLE_NO_BODY_HTML


@app.route('/name', methods=['GET'])
def get_name():
    return "My name is: Master Splinter"


@app.route('/useragent', methods=['GET'])
def get_user_agent():
    return request.user_agent.string


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        buffer = []
        buffer.append("Content-type: %s" % f.content_type)
        buffer.append("File content: %s" % f.stream.read())

        return '|'.join(buffer)


@app.route('/foo')
def foo():
    return "BAR!"


@app.route('/query', methods=['GET'])
def query_string():
    if request.query_string == "model":
        return "query string is valid"
    else:
        abort(500)


@app.route('/popup')
def popup():
    return EXAMPLE_POPUP_HTML

@app.route('/authenticate')
@requires_auth
def auth_required():
    return "Success!"


def start_flask_app(host, port):
    """Runs the server."""
    app.run(host=host, port=port)
    app.config['DEBUG'] = False
    app.config['TESTING'] = False

if __name__ == '__main__':
    app.run()
