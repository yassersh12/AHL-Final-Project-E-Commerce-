from uuid import uuid4, UUID
from datetime import datetime
from typing import Optional, Dict, List
from app.models import User
import bcrypt
from app.api.exceptions.GlobalException import EmailAlreadyExistsException


class UserService:
    def __init__(self):
        self.users: Dict[UUID, User] = {}

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def create_user(self, user: User) -> User:

        if any(
            existing_user.email == user.email for existing_user in self.users.values()
        ):
            raise EmailAlreadyExistsException()

        user_id = str(uuid4())
        user.id = user_id
        user.created_at = datetime.now()
        user.updated_at = None
        self.users[user_id] = user
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def get_all_users(self) -> List[User]:
        return list(self.users.values())

    def update_user(self, user_id: str, updated_user: User) -> Optional[User]:
        current_user = self.users.get(user_id)
        if current_user:
            for existing_user_id, existing_user in self.users.items():
                if (
                    existing_user.email == updated_user.email
                    and existing_user_id != user_id
                ):
                    raise EmailAlreadyExistsException()

            updated_user.id = user_id
            updated_user.updated_at = datetime.now()
            self.users[user_id] = updated_user
            return self.users.get(user_id)
        return None

    def delete_user(self, user_id: str) -> Optional[User]:
        return self.users.pop(user_id, None)
