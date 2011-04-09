from flask import Flask
from flask import request
from multiprocessing import Process
from urllib import urlopen

EXAMPLE_APP = "http://localhost:5000/"

EXAMPLE_HTML = """\
<html>
  <head>
    <title>Example Title</title>
    <script type="text/javascript" src="/static/jquery.min.js"></script>
    <script type="text/javascript">
        $(document).ready(function() {
           $(".add-async-element").click(function() {
                setTimeout(function() {
                    $('body').append('<h4 id="async-header" class="async-element">async elment</h4>');
                    $('body').append('<input type="text" name="async-input" class="async-input" />');
                }, 1200 );
                setTimeout(function() {
                    $('body').append('<h5 id="async-header2" class="async-element2">async elment2</h5>');
                    $('body').append('<input type="text" name="async-input2" class="async-input2" />');
                }, 2400 );
           });

           $(".remove-async-element").click(function() {
                setTimeout(function() {
                    $('.async-element').remove();
                    $('.async-input').remove();
                }, 1200 );
           });

           $(".add-element-mouseover").mouseover(function () {
                $('body').append('<label for="what-is-your-name" class="over-label">What is your name?</label>');
                $('body').append('<input type="text" id="what-is-your-name" class="over-input" name="whatsname" />');
           });

           $(".add-element-mouseover").mouseout(function () {
                $('.over-label').remove();
                $('.over-input').remove();
           });
        });
    </script>
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
    <a class='add-async-element' href="#">add async element</a>
    <a class='remove-async-element' href="#">remove async element</a>
    <a class='add-element-mouseover' href="#">addelement (mouseover)</a>
    <iframe id="iframemodal" src="/iframe"></iframe>
  </body>
</html>"""

EXAMPLE_IFRAME_HTML = """\
<html>
  <head>
    <title>Example Title</title>
  </head>
  <body>
    <h1 id="firstheader">IFrame Example Header</h1>
  </body>
</html>"""

app = Flask(__name__)

@app.route('/')
def index():
    return EXAMPLE_HTML

@app.route('/iframe')
def iframed():
    return EXAMPLE_IFRAME_HTML

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
