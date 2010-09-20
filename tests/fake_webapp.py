from flask import Flask

EXAMPLE_APP = 'http://localhost:5000/'
EXAMPLE_HTML = """\
<html>
  <head>
    <title>Example Title</title>
  </head>
  <body>
    <h1 id="firstheader">Example Header</h1>
    <form action="name" method="GET">
        <label for="query">Query</label>
        <input type="text" name="query" value="default value" />
        <label for="send">Send</label>
        <input type="submit" name="send" />
    </form>
    <a href="http://example.com">Link for Example.com</a>
  </body>
</html>"""

app = Flask(__name__)

@app.route('/')
def index():
    return EXAMPLE_HTML


@app.route('/name', methods=['GET'])
def get_name():
    return "My name is: Master Splinter"


if __name__ == '__main__':
    app.run()
