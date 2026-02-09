from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_utils.cbv import cbv

from auth.auth_service import AuthService
from auth.utils.crypt_utils import get_password_hash, verify_password
from common.dtos.wrapped_response import WrappedResponse
from common.utils.get_services import get_auth_service
from configs.setting import RULE_ENGINE_URL
from user.dtos.user_dtos import UserInfo, UserCreateRequest, UserUpdateRequest, UserPWUpdateRequest
from utils.get_user_id import get_user_id
from utils.proxy_request import proxy_request

user_router = APIRouter(prefix="/user", tags=["회원 서비스 중계"])
security = HTTPBearer()


@cbv(user_router)
class UserHandler:
    base_prefix = "/user"

    @user_router.get(
        "/detail", response_model=WrappedResponse[UserInfo], summary="회원 정보 조회"
    )
    async def get_user(self, auth: HTTPAuthorizationCredentials = Depends(security)):
        user_id: str = get_user_id(auth)
        return await proxy_request(
            "GET",
            RULE_ENGINE_URL,
            f"{self.base_prefix}/{user_id}",
            auth.credentials
        )

    @user_router.post(
        "/create", response_model=WrappedResponse[UserInfo], summary="회원 가입"
    )
    async def create_user(
        self,
        request_data: UserCreateRequest,
        auth_service: AuthService = Depends(get_auth_service),
    ):
        created = await auth_service.signup(
            username=request_data.username,
            hashed_password=get_password_hash(request_data.password),
            email=request_data.email,
        )
        return {
            "data": created,
            "message": f"{request_data.username}님, 가입을 환영합니다!",
        }

    @user_router.put(
        "/update", response_model=WrappedResponse[UserInfo], summary="회원 정보 수정"
    )
    async def update_user(
            self,
            request_data: UserUpdateRequest,
            auth: HTTPAuthorizationCredentials = Depends(security)
    ):
        user_id: str = get_user_id(auth)
        params = {**request_data.model_dump(), "user_id": user_id}
        return await proxy_request(
            "PUT",
            RULE_ENGINE_URL,
            f"{self.base_prefix}/update",
            auth.credentials,
            json=params
        )


    @user_router.patch(
        "/password", response_model=WrappedResponse[int], summary="회원 비밀번호 변경"
    )
    async def update_user_pw(
            self, request_data: UserPWUpdateRequest,
            auth_service: AuthService = Depends(get_auth_service),
            auth: HTTPAuthorizationCredentials = Depends(security)
    ):
        user_id: str = get_user_id(auth)
        user = await auth_service.get_current_user_info(user_id)

        if not user or not verify_password(request_data.old_pw, user["password_hash"]):
            raise HTTPException(
                status_code=401,
                detail="기존 비밀번호가 일치하지 않습니다."
            )

        params = {
            "user_id": int(user_id),
            "password_hash": get_password_hash(request_data.new_pw),
        }
        return await proxy_request(
            "PATCH",
            RULE_ENGINE_URL,
            f"{self.base_prefix}/password",
            auth.credentials,
            json=params
        )


    @user_router.delete(
        "/delete", response_model=WrappedResponse[int], summary="회윈 탈퇴"
    )
    async def delete_user(self, auth: HTTPAuthorizationCredentials = Depends(security)):
        user_id: str = get_user_id(auth)
        return await proxy_request(
            "DELETE",
            RULE_ENGINE_URL,
            f"{self.base_prefix}/delete/{user_id}",
            auth.credentials
        )
