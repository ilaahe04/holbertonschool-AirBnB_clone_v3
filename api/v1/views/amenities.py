#!/usr/bin/python3
"""Amenity"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def retrieves_all_amenities():
    amenities = storage.all("Amenity").values()
    amenities_list = []
    for amenity in amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, "Not a JSON")
    if 'name' not in amenity_data:
        abort(400, "Missing name")
    new_amenity = Amenity(**amenity_data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    amenity_data = request.get_json()
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if not amenity_data:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in amenity_data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
