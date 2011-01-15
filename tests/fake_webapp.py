from flask import Flask
from flask import request
from multiprocessing import Process
from urllib import urlopen

EXAMPLE_APP = "http://localhost:5000/"

EXAMPLE_HTML = """\
<html>
  <head>
    <title>Example Title</title>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script> 
  </head>
  <body>
    <h1 id="firstheader">Example Header</h1>
    <h1 id="firstheader">Example Last Header</h1>
    <form action="name" method="GET">
        <label for="query">Query</label>
        <input type="text" name="query" value="default value" />
        <input type="text" name="query" value="default last value" />
        <label for="send">Send</label>
        <input type="submit" name="send" />
        <input type="radio" name="some-radio" value="choice" />
        <input type="radio" name="other-radio" value="other-choice" />
        <input type="checkbox" name="some-check" value="choice" />
        <input type="checkbox" name="checked-checkbox" value="choosed" checked="checked" />
        <select name="uf">
            <option value="mt">Mato Grosso</option>
            <option value="rj">Rio de Janeiro</option>
        </select>
    </form>
    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="file"> 
        <input type="submit" name="upload" />
    </form>
    <a href="http://example.com">Link for Example.com</a>
    <a href="http://example.com/last">Link for Example.com</a>
    <a href="http://example.com">Link for last Example.com</a>
    <div id="visible">visible</div>
    <div id="invisible" style="display:none">invisible</div>
    <a href="/foo">FOO</a>
  </body>
</html>"""

app = Flask(__name__)

@app.route('/')
def index():
    return EXAMPLE_HTML

@app.route('/name', methods=['GET'])
def get_name():
    return "My name is: Master Splinter"
    
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

class Env(object):
    pass

env = Env()
env.process = None
env.host, env.port = 'localhost', 5000
env.browser = None

def start_flask_app(host, port):
    """Runs the server."""
    app.run(host=host, port=port)
    app.config['DEBUG'] = False
    app.config['TESTING'] = False

def wait_until_start():
    while True:
        try:
            urlopen(EXAMPLE_APP)
            break
        except IOError:
            pass

def wait_until_stop():
    while True:
        try:
            results = urlopen(EXAMPLE_APP)
            if results.code == 404:
                break
        except IOError:
            break

def start_server():
    env.process = Process(target=start_flask_app, args=(env.host, env.port))
    env.process.daemon = True
    env.process.start()
    wait_until_start()

def stop_server():
    env.process.terminate()
    wait_until_stop()
