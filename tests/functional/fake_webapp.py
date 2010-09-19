from flask import Flask

EXAMPLE_APP = 'http://localhost:5000'
app = Flask(__name__)

@app.route('/')
def index():
    return """\
<html>
  <body>
    <head>
      <title>Example Title</title>
    </head>
  </body
</html>"""

if __name__ == '__main__':
    app.run()
