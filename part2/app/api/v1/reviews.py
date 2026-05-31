
"""
Review API.
"""

from flask import request
from flask_restx import (
    Namespace,
    Resource
)

from app.services.facade import HBnBFacade

api = Namespace(
    "reviews",
    description="Review operations"
)

facade = HBnBFacade()


@api.route("/")
class ReviewList(Resource):

    def get(self):

        reviews = facade.get_reviews()

        return [
            review.to_dict()
            for review in reviews
        ], 200

    def post(self):

        data = request.get_json()

        required = [
            "text",
            "user_id",
            "place_id"
        ]

        for field in required:
            if field not in data:
                return {
                    "error":
                    f"{field} is required"
                }, 400

        try:
            review = facade.create_review(
                data
            )

            return (
                review.to_dict(),
                201
            )

        except ValueError as e:
            return {
                "error":
                str(e)
            }, 400


@api.route("/<string:review_id>")
class ReviewResource(Resource):

    def get(
        self,
        review_id
    ):

        review = facade.get_review(
            review_id
        )

        if review is None:
            return {
                "error":
                "Review not found"
            }, 404

        return (
            review.to_dict(),
            200
        )

    def put(
        self,
        review_id
    ):

        review = facade.get_review(
            review_id
        )

        if review is None:
            return {
                "error":
                "Review not found"
            }, 404

        data = request.get_json()

        data.pop(
            "id",
            None
        )

        data.pop(
            "user",
            None
        )

        data.pop(
            "place",
            None
        )

        review = facade.update_review(
            review_id,
            data
        )

        return (
            review.to_dict(),
            200
        )

    def delete(
        self,
        review_id
    ):

        deleted = facade.delete_review(
            review_id
        )

        if not deleted:
            return {
                "error":
                "Review not found"
            }, 404

        return {
            "message":
            "Review deleted"
        }, 200