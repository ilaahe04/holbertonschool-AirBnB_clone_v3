#!/usr/bin/python3
"""It’s time to start your API!"""


from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify


app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(response_or_exc):
    storage.close()

@app.errorhandler(404)
def error_handler(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
