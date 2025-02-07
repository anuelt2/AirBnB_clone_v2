"""Script that starts a Flask web application"""
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def hello():
    """Handle requests to root URL ("/")"""
    return "Hello HBNB!"


@app.route("/hbnb")
def hbnb():
    """Handle requests to "/hbnb" URL"""
    return "HBNB"


@app.route("/c/<text>")
def c(text):
    """Handle requests to "/c/<text>" URL"""
    format_text = text.replace("_", " ")
    return f"C {format_text}"


@app.route("/python")
@app.route("/python/<text>")
def python(text="is cool"):
    """Handle requests to "/python/<text>" URL"""
    format_text = text.replace("_", " ")
    return f"Python {format_text}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
