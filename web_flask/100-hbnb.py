#!/usr/bin/python3
"""Script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_storage(exception=None):
    """Removes current database session after each request"""
    storage.close()


@app.route("/hbnb")
def hbnb():
    """Handle requests to "/hbnb" URL"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)
    for state in states:
        if storage.__class__.__name__ == "DBStorage":
            state.cities = sorted(state.cities, key=lambda city: city.name)
        else:
            state.cities = sorted(state.cities(), key=lambda city: city.name)
    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda amenity: amenity.name)
    places = storage.all(Place).values()
    places = sorted(places, key=lambda place: place.name)
    return render_template(
            "100-hbnb.html",
            states=states,
            amenities=amenities,
            places=places
            )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
