
"""
Place API endpoints.
"""

from flask import request
from flask_restx import (
    Namespace,
    Resource
)

from app.services.facade import HBnBFacade

api = Namespace(
    'places',
    description='Place operations'
)

facade = HBnBFacade()


@api.route('/')
class PlaceList(Resource):

    def get(self):
        """
        Get all places.
        """

        places = facade.get_places()

        return [
            place.to_dict()
            for place in places
        ], 200

    def post(self):
        """
        Create place.
        """

        data = request.get_json()

        required = [
            "title",
            "price",
            "latitude",
            "longitude",
            "owner_id"
        ]

        for field in required:
            if field not in data:
                return {
                    "error":
                    f"{field} is required"
                }, 400

        try:
            place = facade.create_place(
                data
            )

            return (
                place.to_dict(),
                201
            )

        except ValueError as e:

            return {
                "error": str(e)
            }, 400


@api.route('/<string:place_id>')
class PlaceResource(Resource):

    def get(
        self,
        place_id
    ):
        """
        Get place by id.
        """

        place = facade.get_place(
            place_id
        )

        if place is None:
            return {
                "error":
                "Place not found"
            }, 404

        return (
            place.to_dict(),
            200
        )

    def put(
        self,
        place_id
    ):
        """
        Update place.
        """

        place = facade.get_place(
            place_id
        )

        if place is None:
            return {
                "error":
                "Place not found"
            }, 404

        data = request.get_json()

        forbidden = [
            "id",
            "created_at",
            "updated_at",
            "owner",
            "owner_id"
        ]

        for field in forbidden:
            data.pop(
                field,
                None
            )

        try:
            place = facade.update_place(
                place_id,
                data
            )

            return (
                place.to_dict(),
                200
            )

        except ValueError as e:

            return {
                "error":
                str(e)
            }, 400
@api.route(
    '/<string:place_id>/reviews'
)
class PlaceReviews(Resource):

    def get(
        self,
        place_id
    ):

        reviews = facade.get_place_reviews(
            place_id
        )

        return [
            review.to_dict()
            for review in reviews
        ], 200