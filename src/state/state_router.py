from typing import List
from jose import jwt

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_utils.cbv import cbv

from common.dtos.wrapped_response import WrappedResponse
from configs.setting import STATE_MANAGER_URL, SECRET_KEY, ALGORITHM
from state.dtos.state_dtos import FullPlayerState, SessionInfo, SequenceDetailInfo, SessionStartRequest
from utils.proxy_request import proxy_request

state_router = APIRouter(prefix="/state", tags=["게임 상태 중계"])
security = HTTPBearer()


@cbv(state_router)
class StateRouter:
    base_prefix = "/state"

    # Todo: 사용자 게임 세션 생성 - state manager api 추가 확인 후 작업
    # 사용자 게임 세션 생성
    @state_router.post(
        "/session/start", # 임시 라우트 경로
        response_model=WrappedResponse[SessionInfo],
        summary="게임 시작 - 사용자 게임 세션을 생성합니다."
    )
    async def start_session(self, request: SessionStartRequest, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await proxy_request("POST", STATE_MANAGER_URL, f"{self.base_prefix}/session/start", auth.credentials, json=request.model_dump())


    # 사용자 세션 목록 조회
    @state_router.get(
        "/sessions/user",
        response_model = WrappedResponse[List[SessionInfo]],
        summary="사용자 활성 세션 목록을 조회합니다."
    )
    async def get_sessions_by_user_id(self, auth: HTTPAuthorizationCredentials = Depends(security)):
        token = auth.credentials
        # 1. 토큰 복호화 및 유효성 검증
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        return await proxy_request(
            "GET",
            STATE_MANAGER_URL,
        f"{self.base_prefix}/sessions/user/{user_id}",
            auth.credentials
        )

    @state_router.get(
        "/sessions/active",
        response_model=WrappedResponse[List[SessionInfo]],
        summary="전체 활성화 세션 목록을 조회합니다.(FE에서 불필요해 보임)"
    )
    async def get_sessions(self, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await proxy_request("GET", STATE_MANAGER_URL, f"{self.base_prefix}/sessions/active", auth.credentials)


    # 세션 조회
    @state_router.get(
        "/session/{session_id}",
        response_model=WrappedResponse[SessionInfo],
        summary="세션 정보를 조회합니다."
    )
    async def get_session(self, session_id: str, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await proxy_request("GET", STATE_MANAGER_URL, f"{self.base_prefix}/session/{session_id}", auth.credentials)

    # 플레이어 상태 조회
    @state_router.get(
        "/player/{player_id}",
        response_model=WrappedResponse[FullPlayerState],
        summary="플레이어 상태를 조회합니다."
    )
    async def get_player(self, player_id: str, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await proxy_request("GET", STATE_MANAGER_URL, f"{self.base_prefix}/player/{player_id}", auth.credentials)

    # 시퀀스 상세 조회
    @state_router.get(
        "/session/{session_id}/sequence/details",
        response_model=WrappedResponse[SequenceDetailInfo],
        summary="시퀀스 상세 정보를 조회합니다."
    )
    async def get_sequence_details(self, session_id: str, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await proxy_request('GET', STATE_MANAGER_URL, f"{self.base_prefix}/session/{session_id}/sequence/details",  auth.credentials)

