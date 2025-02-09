#!/usr/bin/python3
"""Script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_storage(exception=None):
    """Removes current database session after each request"""
    storage.close()


@app.route("/hbnb_filters")
def hbnb_filters():
    """Handle requests to "/hbnb_filters" URL"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)
    for state in states:
        if storage.__class__.__name__ == "DBStorage":
            state.cities = sorted(state.cities, key=lambda city: city.name)
        else:
            state.cities = sorted(state.cities(), key=lambda city: city.name)
    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda amenity: amenity.name)
    return render_template(
            "10-hbnb_filters.html",
            states=states,
            amenities=amenities
            )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
