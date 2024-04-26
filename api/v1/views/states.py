#!usr/bin/python3
"""State"""


from models.state import State
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def state():
    states = storage.all(State).values()
    list = []
    for state in states:
        list.append(state.to_dict())
    return jsonify(list)


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def state_id(state_id):
    return