
"""
Amenity API endpoints.
"""

from flask import request
from flask_restx import Namespace, Resource

from app.services.facade import HBnBFacade

api = Namespace(
    'amenities',
    description='Amenity operations'
)

facade = HBnBFacade()


@api.route('/')
class AmenityList(Resource):
    """
    Handle amenity collection.
    """

    def get(self):
        """
        Retrieve all amenities.
        """

        amenities = facade.get_amenities()

        return [
            amenity.to_dict()
            for amenity in amenities
        ], 200

    def post(self):
        """
        Create amenity.
        """

        data = request.get_json()

        if not data:
            return {
                "error": "Invalid JSON"
            }, 400

        if "name" not in data:
            return {
                "error": "name is required"
            }, 400

        amenity = facade.create_amenity(data)

        return amenity.to_dict(), 201


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    """
    Handle single amenity.
    """

    def get(self, amenity_id):
        """
        Retrieve amenity.
        """

        amenity = facade.get_amenity(
            amenity_id
        )

        if amenity is None:
            return {
                "error": "Amenity not found"
            }, 404

        return amenity.to_dict(), 200

    def put(self, amenity_id):
        """
        Update amenity.
        """

        amenity = facade.get_amenity(
            amenity_id
        )

        if amenity is None:
            return {
                "error": "Amenity not found"
            }, 404

        data = request.get_json()

        if not data:
            return {
                "error": "Invalid JSON"
            }, 400

        data.pop("id", None)
        data.pop("created_at", None)
        data.pop("updated_at", None)

        amenity = facade.update_amenity(
            amenity_id,
            data
        )

        return amenity.to_dict(), 200