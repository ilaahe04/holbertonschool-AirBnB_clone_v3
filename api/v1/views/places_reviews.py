#!/usr/bin/python3
"""Places_reviews"""


from models.review import Review
from models.place import Place
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage


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
def create_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    review_data = request.get_json()
    if not review_data:
        abort(400, "Not a JSON")
    new_review = Review(**review_data)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


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
