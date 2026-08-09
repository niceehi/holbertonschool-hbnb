```python
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade


api = Namespace("places", description="Place operations")


amenity_model = api.model("PlaceAmenity", {
    "id": fields.String(description="Amenity ID"),
    "name": fields.String(description="Name of the amenity")
})


owner_model = api.model("PlaceUser", {
    "id": fields.String(description="User ID"),
    "first_name": fields.String(description="First name of the owner"),
    "last_name": fields.String(description="Last name of the owner"),
    "email": fields.String(description="Email of the owner")
})


place_model = api.model("Place", {
    "title": fields.String(
        required=True,
        description="Title of the place"
    ),
    "description": fields.String(
        description="Description of the place"
    ),
    "price": fields.Float(
        required=True,
        description="Price per night"
    ),
    "latitude": fields.Float(
        required=True,
        description="Latitude of the place"
    ),
    "longitude": fields.Float(
        required=True,
        description="Longitude of the place"
    ),
    "amenities": fields.List(
        fields.String,
        description="List of amenities ID's"
    )
})


@api.route("/")
class PlaceList(Resource):

    @api.expect(place_model)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @api.response(401, "Unauthorized")
    @api.doc(security="apikey")
    @jwt_required()
    def post(self):
        """Register a new place"""

        data = api.payload
        owner_id = get_jwt_identity()

        try:
            created_place = facade.create_place(data, owner_id)
            return created_place.to_dict(), 201

        except Exception as error:
            return {"error": str(error).strip("'")}, 400

    @api.response(200, "List of places retrieved successfully")
    def get(self):
        """Retrieve a list of all places"""

        all_places = facade.get_all_places()

        return [
            item.to_dict_list()
            for item in all_places
        ], 200


@api.route("/<place_id>")
class PlaceResource(Resource):

    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get place details by ID"""

        selected_place = facade.get_place(place_id)

        if selected_place is None:
            return {"error": "Place not found"}, 404

        return selected_place.to_dict_list(), 200

    @api.expect(place_model)
    @api.response(200, "Place updated successfully")
    @api.response(404, "Place not found")
    @api.response(400, "Invalid input data")
    @api.response(401, "Unauthorized")
    @api.response(403, "Forbidden")
    @api.doc(security="apikey")
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""

        changes = api.payload
        user_id = get_jwt_identity()
        selected_place = facade.get_place(place_id)
        claims = get_jwt()
        is_admin = claims["is_admin"]

        if selected_place is None:
            return {"error": "Place not found"}, 404

        if selected_place.owner.id != user_id and not is_admin:
            return {"error": "Forbidden"}, 403

        try:
            updated_place = facade.update_place(
                place_id,
                changes
            )

            return updated_place.to_dict(), 200

        except Exception as error:
            return {"error": str(error).strip("'")}, 400

    @api.response(200, "Place deleted successfully")
    @api.response(404, "Place not found")
    @api.response(401, "Unauthorized")
    @api.response(403, "Forbidden")
    @api.doc(security="apikey")
    @jwt_required()
    def delete(self, place_id):
        """Update a place's information"""

        user_id = get_jwt_identity()
        selected_place = facade.get_place(place_id)
        claims = get_jwt()
        is_admin = claims["is_admin"]

        if selected_place is None:
            return {"error": "Place not found"}, 404

        if selected_place.owner.id != user_id and not is_admin:
            return {"error": "Forbidden"}, 403

        try:
            facade.delete_place(place_id)

            return {
                "message": "Place deleted successfully"
            }, 200

        except Exception as error:
            return {"error": str(error).strip("'")}, 400


@api.route("/<place_id>/amenities")
class PlaceAmenities(Resource):

    @api.expect(amenity_model)
    @api.response(200, "Amenities added successfully")
    @api.response(404, "Place not found")
    @api.response(400, "Invalid input data")
    def post(self, place_id):
        """Add amenities to a place"""

        amenities = api.payload

        if not amenities or len(amenities) == 0:
            return {"error": "Invalid input data"}, 400

        selected_place = facade.get_place(place_id)

        if selected_place is None:
            return {"error": "Place not found"}, 404

        for item in amenities:
            amenity = facade.get_amenity(item["id"])

            if amenity is None:
                return {"error": "Invalid input data"}, 400

        for item in amenities:
            selected_place.add_amenity(item)

        return {
            "message": "Amenities added successfully"
        }, 200


@api.route("/<place_id>/reviews/")
class PlaceReviewList(Resource):

    @api.response(
        200,
        "List of reviews for the place retrieved successfully"
    )
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get all reviews for a specific place"""

        selected_place = facade.get_place(place_id)

        if selected_place is None:
            return {"error": "Place not found"}, 404

        return [
            review.to_dict()
            for review in selected_place.reviews
        ], 200
```
