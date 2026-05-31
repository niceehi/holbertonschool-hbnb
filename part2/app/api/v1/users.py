from flask_restx import Namespace, Resource

api = Namespace('users', description='Users operations')

from app.services.facade import HBnBFacade

facade = HBnBFacade()


@api.route('/')
class UserList(Resource):

    def get(self):

        users = facade.get_users()

        return [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
            }
            for user in users
        ]

    def post(self):

        from flask import request

        data = request.json

        user = facade.create_user(data)

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }, 201