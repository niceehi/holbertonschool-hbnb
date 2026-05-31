from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:

    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, data):

        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"]
        )

        self.user_repo.add(user)

        return user

    def get_users(self):
        return self.user_repo.get_all()