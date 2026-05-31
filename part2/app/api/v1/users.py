
"""
Users endpoints.
"""

from flask import request
from flask_restx import Namespace, Resource

from app.services.facade import HBnBFacade

api = Namespace(
    'users',
    description='User operations'
)

facade = HBnBFacade()


@api.route('/')
class UserList(Resource):

    def get(self):
        """
        Retrieve all users.
        """

        users = facade.get_users()

        return [
            user.to_dict()
            for user in users
        ], 200

    def post(self):
        """
        Create a new user.
        """

        data = request.get_json()

        required = [
            "first_name",
            "last_name",
            "email",
            "password"
        ]

        for field in required:
            if field not in data:
                return {
                    "error": f"{field} is required"
                }, 400

        user = facade.create_user(data)

        return user.to_dict(), 201


@api.route('/<string:user_id>')
class UserResource(Resource):

    def get(self, user_id):
        """
        Retrieve user by id.
        """

        user = facade.get_user(user_id)

        if not user:
            return {
                "error": "User not found"
            }, 404

        return user.to_dict(), 200

    def put(self, user_id):
        """
        Update user.
        """

        user = facade.get_user(user_id)

        if not user:
            return {
                "error": "User not found"
            }, 404

        data = request.get_json()

        forbidden_fields = [
            "id",
            "created_at",
            "updated_at"
        ]

        for field in forbidden_fields:
            data.pop(field, None)

        updated_user = facade.update_user(
            user_id,
            data
        )

        return updated_user.to_dict(), 200