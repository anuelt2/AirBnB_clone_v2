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


@app.route("/cities_by_states")
def cities_by_states():
    """Handles requests to "/cities_by_states" URL"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)
    for state in states:
        if storage.__class__.__name__ == "DBStorage":
            state.cities = sorted(state.cities, key=lambda city: city.name)
        else:
            state.cities = sorted(state.cities(), key=lambda city: city.name)
    return render_template("8-cities_by_states.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
