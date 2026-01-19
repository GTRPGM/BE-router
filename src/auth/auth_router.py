from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_utils.cbv import cbv
from jose import jwt, ExpiredSignatureError, JWTError

from common.dtos.wrapped_response import WrappedResponse
from common.utils.get_services import get_auth_service
from configs.setting import ALGORITHM, SECRET_KEY
from src.auth.auth_service import AuthService
from src.auth.dtos.login_dtos import LoginRequest, Token  # 정의하신 DTO 임포트
from src.configs.database import get_db_cursor

auth_router = APIRouter(prefix="/auth", tags=["인증 및 로그인"])
auth_scheme = HTTPBearer()

@cbv(auth_router)
class AuthHandler:
    @auth_router.post(
        "/login",
        summary="로그인",
        response_model=WrappedResponse[Token],
    )
    async def login(
            self,
            login_data: LoginRequest,
            auth_service: AuthService = Depends(get_auth_service)
    ):
        with get_db_cursor() as cursor:
            # 서비스에 DTO 데이터 전달
            auth_result = auth_service.authenticate_user(
                login_data.username, login_data.password
            )

            return {
                "data": auth_result,
                "message": f"{login_data.username}님, 환영합니다!",
            }

    @auth_router.get(
        "/me",
        summary="현재 로그인 상태 및 정보 확인",
        response_model=WrappedResponse[Dict[str, Any]],  # 필요시 UserResponse DTO 사용
    )
    async def get_me(
            self,
            token_auth: HTTPAuthorizationCredentials = Depends(auth_scheme),
            auth_service: AuthService = Depends(get_auth_service)
    ):
        try:
            token = token_auth.credentials
            # 1. 토큰 복호화 및 유효성 검증
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")

            if user_id is None:
                raise ValueError("유효하지 않은 토큰이 제공되었습니다.")

            # 2. 서비스 계층에서 유저 정보 조회
            user_info = auth_service.get_current_user_info(user_id)

            return {
                "data": user_info,
                "message": "인증되었습니다."
            }

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="토큰이 만료되었습니다.")
        except Exception as e:
            raise HTTPException(status_code=401, detail="인증에 실패했습니다.")


    @auth_router.post("/logout")
    async def logout(
            self,
            # HTTPBearer를 통해 'Bearer ' 접두사를 떼고 토큰 값만 가져옴
            token_auth: HTTPAuthorizationCredentials = Depends(auth_scheme),
            auth_service: AuthService = Depends(get_auth_service)
    ):
        try:
            # 이미 Bearer가 제거된 순수 토큰 값
            token = token_auth.credentials

            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")

            with get_db_cursor() as cursor:
                auth_service.process_logout(user_id)

            return {"data": None, "message": "성공적으로 로그아웃되었습니다."}
        except Exception:
            raise HTTPException(
                status_code=401, detail="유효하지 않은 토큰이거나 로그아웃 중 오류가 발생했습니다."
            )
