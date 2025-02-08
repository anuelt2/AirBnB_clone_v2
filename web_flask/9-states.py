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


@app.route("/states")
def states():
    """Handle requests to "/states" URL"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)
    return render_template("9-states.html", states=states, path="state")


@app.route("/states/<id>")
def states_id(id):
    """Handle requests to "/states/<id>" URL"""
    state = storage.all(State).get(f"State.{id}")
    if state:
        if storage.__class__.__name__ == "DBStorage":
            cities = sorted(state.cities, key=lambda city: city.name)
        else:
            cities = sorted(state.cities(), key=lambda city: city.name)
    else:
        return render_template("9-states.html", path="none")
    return render_template(
            "9-states.html",
            state=state,
            cities=cities,
            path="state_id"
            )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
