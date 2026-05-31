
"""
Amenity model.
"""

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Represents an amenity.
    """

    def __init__(self, name):
        """
        Initialize amenity.
        """
        super().__init__()

        if not name:
            raise ValueError("Amenity name is required")

        self.name = name

    def to_dict(self):
        """
        Convert amenity to dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }