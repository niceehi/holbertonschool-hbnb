```python
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

import config

from app.api.v1.auth import api as auth_api
from app.api.v1.amenities import api as amenities_api
from app.api.v1.places import api as places_api
from app.api.v1.protected import api as protected_api
from app.api.v1.reviews import api as reviews_api
from app.api.v1.users import api as users_api


bcrypt = Bcrypt()
jwt_manager = JWTManager()
database = SQLAlchemy()


def create_app(config_class=config.DevelopmentConfig):
    """Create and configure the Flask application."""

    application = Flask(__name__)
    CORS(application)

    application.config.from_object(config_class)

    # Initialize Flask extensions
    bcrypt.init_app(application)
    jwt_manager.init_app(application)
    database.init_app(application)

    authorization_config = {
        "apikey": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": (
                "Type in the *'Value'* input box below: "
                "**'Bearer <JWT>'**, where JWT is the token"
            )
        }
    }

    api = Api(
        application,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        authorizations=authorization_config
    )

    namespaces = [
        (users_api, "/api/v1/users"),
        (amenities_api, "/api/v1/amenities"),
        (places_api, "/api/v1/places"),
        (reviews_api, "/api/v1/reviews"),
        (auth_api, "/api/v1/auth"),
        (protected_api, "/api/v1/protected"),
    ]

    for namespace, path in namespaces:
        api.add_namespace(namespace, path=path)

    return application
```
