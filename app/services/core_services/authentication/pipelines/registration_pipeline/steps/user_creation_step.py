from app.repositories.authentication_repositories.user_repository import UserRepository
from app.services.model_schema_services.user_service import UserService


class UserCreationStep:
    def __init__(self):
        self.user_service = UserService(UserRepository())