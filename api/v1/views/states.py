#!/usr/bin/python3
"""State"""


from models.state import State
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    states = [state.to_dict() for state in storage.all("State").values()]
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    state_data = request.get_json()
    if not state_data:
        abort(400, "Not a JSON")
    if 'name' not in state_data:
        abort(400, "Missing name")
    new_state = State(**state_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    state_data = request.is_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not state_data:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in state_data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
