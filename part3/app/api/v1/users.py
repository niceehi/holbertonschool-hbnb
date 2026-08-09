```python
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from app.services import facade


api = Namespace("users", description="User operations")


user_model = api.model("User", {
    "first_name": fields.String(
        required=True,
        description="First name of the user"
    ),
    "last_name": fields.String(
        required=True,
        description="Last name of the user"
    ),
    "email": fields.String(
        required=True,
        description="Email of the user"
    ),
    "password": fields.String(
        required=True,
        description="Password of the user"
    ),
    "is_admin": fields.Boolean(
        description="Admin status of the user",
        default=False
    )
})


@api.route("/")
class UserList(Resource):

    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Email already registered")
    @api.response(400, "Invalid input data")
    @jwt_required(optional=True)
    def post(self):
        """Register a new user."""

        data = api.payload
        requested_admin = data.get("is_admin", None)

        if requested_admin:
            identity = get_jwt_identity()

            if not identity:
                return {"error": "Unauthorized"}, 401

            claims = get_jwt()
            admin_user = claims["is_admin"]

            print(admin_user)

            if not admin_user:
                return {"error": "Forbidden"}, 403

        existing = facade.get_user_by_email(data["email"])

        if existing:
            return {"error": "Email already registered"}, 400

        try:
            created = facade.create_user(data)

            return {
                "message": "User successfully created",
                "id": created.id
            }, 201

        except Exception as error:
            return {
                "error": str(error).strip("'")
            }, 400

    @api.response(200, "List of users retrieved successfully")
    def get(self):
        """Retrieve a list of users."""

        users_list = facade.get_users()

        return [
            item.to_dict()
            for item in users_list
        ], 200


@api.route("/<user_id>")
class UserResource(Resource):

    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    def get(self, user_id):
        """Get user details by ID."""

        target_user = facade.get_user(user_id)

        if target_user is None:
            return {"error": "User not found"}, 404

        return target_user.to_dict(), 200

    @api.expect(user_model)
    @api.response(200, "User updated successfully")
    @api.response(404, "User not found")
    @api.response(400, "Invalid input data")
    @api.response(401, "Unauthorized")
    @api.response(403, "Forbidden")
    @api.doc(security="apikey")
    @jwt_required()
    def put(self, user_id):
        """Update user information."""

        requester_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims["is_admin"]

        if requester_id != user_id and not is_admin:
            return {"error": "Forbidden"}, 403

        update_data = api.payload

        if not is_admin and update_data.get("is_admin"):
            return {"error": "Forbidden"}, 403

        if not is_admin and (
            update_data.get("email")
            or update_data.get("password")
        ):
            return {
                "error": "You cannot modify email or password."
            }, 400

        target_user = facade.get_user(user_id)

        if target_user is None:
            return {"error": "User not found"}, 404

        try:
            facade.update_user(user_id, update_data)

            return target_user.to_dict(), 200

        except Exception as error:
            return {
                "error": str(error).strip("'")
            }, 400
```
