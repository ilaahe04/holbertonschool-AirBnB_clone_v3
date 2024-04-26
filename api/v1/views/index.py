#!/usr/bin/python3
"""index.py"""


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def stats():
    
    return jsonify({"Amenity": storage.count(Amenity),
                    "City": storage.count(City),
                    "Place": storage.count(Place),
                    "Review": storage.count(Review),
                    "State": storage.count(State),
                    "User": storage.count(User)})