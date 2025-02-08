#!/usr/bin/python3
"""Script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_storage(exception=None):
    """Removes current database session after each request"""
    storage.close()


@app.route("/states_list")
def states_list():
    """Handle requests to "/states_list" URL"""
    states = storage.all(State)
    return render_template("7-states_list.html", states=states.values())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
