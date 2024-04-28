#!/usr/bin/python3
"""cities"""

from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cities(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    if not request.is_json:
        abort(400, "Not a JSON")
    city_data = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if 'name' not in city_data:
        abort(400, "Missing name")
    city_data["state_id"] = state_id
    new_city = City(**city_data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    if not request.is_json:
        abort(400, "Not a JSON")
    city_data = request.get_json()
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in city_data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
