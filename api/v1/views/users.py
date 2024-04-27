#!/usr/bin/python3
"""Flask application for User class"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def retrieves_all_users():
    users = storage.all(User).values()
    users_list = []
    for user in users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    user_data = request.get_json()
    if not user_data:
        abort(400, "Not a JSON")
    elif "email" not in user_data:
        abort(400, "Missing email")
    elif "password" not in user_data:
        abort(400, "Missing password")
    new_user = User(**user_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    user_data = request.get_json()
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not user_data:
        abort(400, "Not a JSON")

    ignore_keys = ["id", "email", "created_at", "updated_at"]
    for key, value in user_data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
