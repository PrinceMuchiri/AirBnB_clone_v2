#!/usr/bin/python3
""" This script starts a Flask web application """
from flask import Flask, escape, render_template

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def route():
    """Returns Hello HBNB"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def route_hbnb():
    """Returns HBNB"""
    return "HBNB"


@app.route("/c/<path:text>", strict_slashes=False)
def c(text):
    """Returns C with text passed to the URL"""
    return "C {}".format(escape(text).replace("_", " "))


@app.route("/python", defaults={"text": "is cool"}, strict_slashes=False)
@app.route("/python/<path:text>", strict_slashes=False)
def python(text):
    """
    Returns Python with text passed to URL
    Defaults text to "is cool" if no text is passed to URL
    """
    return "Python {}".format(escape(text).replace("_", " "))


@app.route("/number/<int:num>", strict_slashes=False)
def route_number(num):
    """Returns "n is a number" only if num is a int"""
    return "{} is a number".format(escape(num))


@app.route("/number_template/<int:n>", strict_slashes=False)
def route_template(n):
    """Returns a HTML page only if num is a int"""
    return render_template("5-number.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
