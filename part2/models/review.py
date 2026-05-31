
"""
Review model.
"""

from app.models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class.
    """

    def __init__(self, text, user, place):
        super().__init__()

        if not text:
            raise ValueError("Review text is required")

        self.text = text
        self.user = user
        self.place = place

    def to_dict(self):
        """
        Convert review to dictionary.
        """

        return {
            "id": self.id,
            "text": self.text,
            "user": {
                "id": self.user.id,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name
            },
            "place": {
                "id": self.place.id,
                "title": self.place.title
            },
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }