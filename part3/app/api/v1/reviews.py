```python
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from app.services import facade


api = Namespace("amenities", description="Amenity operations")


amenity_model = api.model("Amenity", {
    "name": fields.String(
        required=True,
        description="Name of the amenity"
    )
})


@api.route("/")
class AmenityList(Resource):

    @api.expect(amenity_model)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    @api.response(401, "Unauthorized")
    @api.response(403, "Forbidden")
    @api.doc(security="apikey")
    @jwt_required()
    def post(self):
        """Register a new amenity."""

        user_id = get_jwt_identity()

        if not user_id:
            return {"error": "Unauthorized"}, 401

        token_data = get_jwt()
        admin_access = token_data["is_admin"]

        print(user_id, admin_access)

        if not admin_access:
            return {"error": "Forbidden"}, 403

        data = api.payload

        existing = facade.amenity_repo.get_by_attribute(
            "name",
            data.get("name")
        )

        if existing:
            return {"error": "Invalid input data"}, 400

        try:
            amenity = facade.create_amenity(data)

            return amenity.to_dict(), 201

        except Exception as error:
            return {
                "error": str(error).strip("'")
            }, 400

    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        """Retrieve all amenities."""

        result = facade.get_all_amenities()

        return [
            item.to_dict()
            for item in result
        ], 200


@api.route("/<amenity_id>")
class AmenityResource(Resource):

    @api.response(200, "Amenity details retrieved successfully")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        """Get amenity details by ID."""

        selected = facade.get_amenity(amenity_id)

        if selected is None:
            return {"error": "Amenity not found"}, 404

        return selected.to_dict(), 200

    @api.expect(amenity_model)
    @api.response(200, "Amenity updated successfully")
    @api.response(404, "Amenity not found")
    @api.response(400, "Invalid input data")
    @api.response(401, "Unauthorized")
    @api.response(403, "Forbidden")
    @api.doc(security="apikey")
    @jwt_required()
    def put(self, amenity_id):
        """Update an existing amenity."""

        user_id = get_jwt_identity()

        if not user_id:
            return {"error": "Unauthorized"}, 401

        token_data = get_jwt()

        if not token_data["is_admin"]:
            return {"error": "Forbidden"}, 403

        data = api.payload
        selected = facade.get_amenity(amenity_id)

        if selected is None:
            return {"error": "Amenity not found"}, 404

        try:
            changed = facade.update_amenity(
                amenity_id,
                data
            )

            return changed.to_dict(), 200

        except Exception as error:
            return {
                "error": str(error).strip("'")
            }, 400
```
