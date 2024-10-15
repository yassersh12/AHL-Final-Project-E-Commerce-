from pydantic import BaseModel
from uuid import UUID


class TokenData(BaseModel):
    username: UUID | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


# this user modle only for security part, I will change it when I merge it with user branch
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    active: bool | None = None


class UserInDB(User):
    hashed_password: str
