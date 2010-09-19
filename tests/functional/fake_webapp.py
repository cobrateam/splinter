from flask import Flask

EXAMPLE_APP = 'http://localhost:5000'
app = Flask(__name__)

@app.route('/')
def index():
    return """
        <html>
            <head>
              <title>Example Title</title>
            </head>
        </html>"""

if __name__ == '__main__':
    app.run()
