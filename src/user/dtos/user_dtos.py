from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserInfo(BaseModel):
    user_id: Optional[int] = None
    username: str
    email: str
    created_at: Optional[datetime] = None


class UserUpdateRequest(BaseModel):
    username: str
    email: str


class UserPWUpdateRequest(BaseModel):
    old_pw: str
    new_pw: str  # -> password_hash: str


class UserCreateRequest(BaseModel):
    username: str
    password: str  # -> password_hash: str
    email: str
