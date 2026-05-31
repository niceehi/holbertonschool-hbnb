
"""
HBnB Facade.
"""

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review


class HBnBFacade:
    """
    Facade class.
    """

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

    def create_review(self, data):
        """
        Create a review.
        """

        user = self.user_repo.get(
            data["user_id"]
        )

        place = self.place_repo.get(
            data["place_id"]
        )

        if user is None:
            raise ValueError(
                "User not found"
            )

        if place is None:
            raise ValueError(
                "Place not found"
            )

        review = Review(
            data["text"],
            user,
            place
        )

        self.review_repo.add(review)

        place.reviews.append(review)

        return review

    def get_review(self, review_id):
        """
        Get review by id.
        """

        return self.review_repo.get(
            review_id
        )

    def get_reviews(self):
        """
        Get all reviews.
        """

        return self.review_repo.get_all()

    def update_review(
        self,
        review_id,
        data
    ):
        """
        Update review.
        """

        return self.review_repo.update(
            review_id,
            data
        )

    def delete_review(
        self,
        review_id
    ):
        """
        Delete review.
        """

        return self.review_repo.delete(
            review_id
        )

    def get_place_reviews(
        self,
        place_id
    ):
        """
        Get reviews for a place.
        """

        place = self.place_repo.get(
            place_id
        )

        if place:
            return place.reviews

        return []