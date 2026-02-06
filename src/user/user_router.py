from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_utils.cbv import cbv
from jose import jwt

from common.dtos.wrapped_response import WrappedResponse
from user.dtos.user_dtos import UserInfo, UserCreateRequest, UserUpdateRequest
from utils.proxy_request import proxy_request
from configs.setting import RULE_ENGINE_URL, SECRET_KEY, ALGORITHM

user_router = APIRouter(prefix="/user", tags=["회원 서비스 중계"])
security = HTTPBearer()


@cbv(user_router)
class UserHandler:
    base_prefix = "/user"

    @user_router.get(
        "/", response_model=WrappedResponse[UserInfo], summary="회원 정보 조회"
    )
    async def get_user(self, auth: HTTPAuthorizationCredentials = Depends(security)):
        token = auth.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        return await proxy_request("POST", RULE_ENGINE_URL, f"{self.base_prefix}/{user_id}", auth.credentials)

    @user_router.post(
        "/create", response_model=WrappedResponse[UserInfo], summary="회원 가입"
    )
    async def create_user(self, request_data: UserCreateRequest, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await proxy_request("POST", RULE_ENGINE_URL, f"{self.base_prefix}/create", auth.credentials,
                                   json=request_data.model_dump())

    @user_router.post(
        "/update", response_model=WrappedResponse[UserInfo], summary="회원 정보 수정"
    )
    async def update_user(self, request_data: UserUpdateRequest, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await proxy_request("POST", RULE_ENGINE_URL, f"{self.base_prefix}/update", auth.credentials,
                                   json=request_data.model_dump())

    @user_router.delete(
        "/delete/", response_model=WrappedResponse[int], summary="회윈 탈퇴"
    )
    async def delete_user(self, auth: HTTPAuthorizationCredentials = Depends(security)):
        token = auth.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        return await proxy_request("POST", RULE_ENGINE_URL, f"{self.base_prefix}/delete/{user_id}", auth.credentials)
