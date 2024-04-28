#!/usr/bin/python3
"""Places_reviews"""


from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/api/v1/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def get_reviews_by_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/api/v1/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/api/v1/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/api/v1/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def place_reviews(place_id=None, review_id=None):
    """Retrieve places"""
    status_code = 200
    if request.method == 'POST':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        new_review = request.get_json(silent=True)
        if new_review is None:
            abort(400, "Not a JSON")
        elif "text" not in new_review:
            abort(400, "Missing text")
        elif "user_id" not in new_review:
            abort(400, "Missing user_id")
        user = storage.get(User, new_review['user_id'])
        if user is None:
            abort(404)
        new_review['place_id'] = place_id
        new_review = Review(**new_review)
        new_review.save()
        review_id = new_review.id
        status_code = 201
    if review_id:
        response = storage.get(Review, review_id)
        if response is None:
            abort(404)


@app_views.route("/api/v1/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    if not request.is_json:
        abort(400, "Not a JSON")
    review_data = request.get_json()
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    ignore_keys = ["id", "place_id", "user_id", "created_at", "updated_at"]
    for key, value in review_data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
