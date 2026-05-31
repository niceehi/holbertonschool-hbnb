
"""
Place model.
"""

from app.models.base_model import BaseModel
from app.models.place import Place


class Place(BaseModel):
    """
    Represents a place.
    """
    self.reviews = []

    def __init__(
            
            
        self,
        title,
        description,
        price,
        latitude,
        longitude,
        owner,
        amenities=None
    ):
        self.place_repo = InMemoryRepository()
        super().__init__()

        if not title:
            raise ValueError("title is required")

        if price < 0:
            raise ValueError("price must be positive")

        if latitude < -90 or latitude > 90:
            raise ValueError(
                "latitude must be between -90 and 90"
            )

        if longitude < -180 or longitude > 180:
            raise ValueError(
                "longitude must be between -180 and 180"
            )

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

        self.owner = owner
        self.amenities = amenities or []

    def to_dict(self):
        """
        Convert place to dictionary.
        """

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,

            "owner": {
                "id": self.owner.id,
                "first_name": self.owner.first_name,
                "last_name": self.owner.last_name,
                "email": self.owner.email
            },

            "amenities": [
                amenity.to_dict()
                for amenity in self.amenities
            ],

            "created_at":
                self.created_at.isoformat(),

            "updated_at":
                self.updated_at.isoformat()
        }