#!/usr/bin/python3
'''code of Place'''

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_with_id(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return {"error": "Not found"}, 404
    return [place.to_dict() for place in city.places]


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return {"error": "Not found"}, 404
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return {"error": "Not found"}, 404
    storage.delete(place)
    storage.save()
    return {}, 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return {"error": "Not found"}, 404
    data = request.get_json(silent=True)
    if data is None:
        return {"error": "Not a JSON"}, 400
    if "user_id" not in data:
        return {"error": "Missing user_id"}, 400
    user = storage.get(User, data["user_id"])
    if user is None:
        return {"error": "Not found"}, 404
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    data['city_id'] = city_id
    places = Place(**data)
    storage.new(places)
    return jsonify(places.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    data = request.get_json(silent=True)
    place = storage.get(Place, place_id)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if place is None:
        return abort(404)
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
