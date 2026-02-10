from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt, JWTError, ExpiredSignatureError

from configs.setting import ALGORITHM, SECRET_KEY


def get_user_id(auth: HTTPAuthorizationCredentials):
    token = auth.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 인증 정보입니다.",
            )
        return user_id
    except ExpiredSignatureError:
        # 토큰 만료 시
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인 세션이 만료되었습니다. 다시 로그인해주세요.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        # 그 외 토큰 변조 등 에러 시
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증에 실패하였습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id
