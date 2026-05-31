#!/usr/bin/env python3
"""
User model.
"""

from app.models.base_model import BaseModel


class User(BaseModel):
    """
    Represents a user.
    """

    def __init__(self,
                 first_name,
                 last_name,
                 email):
        super().__init__()

        if not first_name:
            raise ValueError("first_name is required")

        if not last_name:
            raise ValueError("last_name is required")

        if not email:
            raise ValueError("email is required")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email

        self.places = []
        self.reviews = []

    def add_place(self, place):
        """
        Add a place owned by user.
        """
        self.places.append(place)
        self.save()

    def add_review(self, review):
        """
        Add review created by user.
        """
        self.reviews.append(review)
        self.save()

    def to_dict(self):
        """
        Return serializable dict.
        Password excluded.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }