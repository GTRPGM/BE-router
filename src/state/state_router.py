from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_utils.cbv import cbv

from common.dtos.wrapped_response import WrappedResponse
from configs.setting import STATE_MANAGER_URL
from state.dtos.state_dtos import FullPlayerState, SessionInfo, SequenceDetailInfo
from utils.proxy_request import proxy_request

state_router = APIRouter(prefix="/state", tags=["게임 상태 중계"])
security = HTTPBearer()


@cbv(state_router)
class StateRouter:
    base_prefix = "/state"

    # Todo: 사용자 게임 세션 생성 - state manager api 추가 확인 후 작업
    @state_router.post(
        "/session/create", # 임시 라우트 경로
        response_model=WrappedResponse[SessionInfo],
        summary="사용자 게임 세션을 생성합니다.(개발중)"
    )
    async def add_session(self, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await proxy_request("POST", STATE_MANAGER_URL, f"{self.base_prefix}/session/create", auth.credentials)

    @state_router.get(
        "/sessions/active",
        response_model=WrappedResponse[List[SessionInfo]],
        summary="사용자의 활성화 세션 목록을 조회합니다.(수정중)"
    )
    # Fixme: 황성화 세션 목록 조회 - user_id 추가 전달(state manager api request 모델 새로 추가 예정)
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

