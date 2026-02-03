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

    # 황성화 세션 목록 조회
    @state_router.get(
        "/sessions/active",
        response_model=WrappedResponse[List[SessionInfo]],
        summary="활성화 세션 목록을 조회합니다."
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
        print(f"{self.base_prefix}/session/{session_id}/sequence/details")
        return await proxy_request('GET', STATE_MANAGER_URL, f"{self.base_prefix}/session/{session_id}/sequence/details",  auth.credentials)

