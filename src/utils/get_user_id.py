from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt

from configs.setting import SECRET_KEY, ALGORITHM


def get_user_id(auth: HTTPAuthorizationCredentials):
    token = auth.credentials
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id: str = payload.get("sub")
    return user_id