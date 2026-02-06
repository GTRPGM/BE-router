from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_utils.cbv import cbv
from jose import jwt

from common.dtos.wrapped_response import WrappedResponse
from configs.setting import STATE_MANAGER_URL, SECRET_KEY, ALGORITHM, RULE_ENGINE_URL
from state.dtos.state_dtos import FullPlayerState, SessionInfo, SequenceDetailInfo, SessionStartRequest, ScenarioInfo, \
    PaginatedSessionResponse
from utils.get_user_id import get_user_id
from utils.proxy_request import proxy_request

state_router = APIRouter(prefix="/state", tags=["게임 상태 중계"])
security = HTTPBearer()


@cbv(state_router)
class StateRouter:
    base_prefix = "/state"

    # 시나리오 조회
    @state_router.get(
        "/scenarios",
        response_model = WrappedResponse[List[ScenarioInfo]],
        summary="시나리오 조회 - 게임 시작에 필요한 scenario_id를 가져올 수 있습니다."
    )
    async def get_scenarios(self, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await proxy_request("GET", STATE_MANAGER_URL, f"{self.base_prefix}/scenarios", auth.credentials)


    # 사용자 게임 세션 생성
    @state_router.post(
        "/session/start", # 임시 라우트 경로
        response_model=WrappedResponse[SessionInfo],
        summary="게임 시작 - 사용자 게임 세션을 생성합니다."
    )
    async def start_session(self, request: SessionStartRequest, auth: HTTPAuthorizationCredentials = Depends(security)):
        user_id: str = get_user_id(auth)
        params = {**request.model_dump(), "user_id": user_id}
        return await proxy_request("POST", STATE_MANAGER_URL, f"{self.base_prefix}/session/start", auth.credentials, json=params)


    # 사용자 세션 목록 조회
    @state_router.get(
        "/session/list",
        response_model = WrappedResponse[PaginatedSessionResponse],
        summary="사용자 활성 세션 목록을 조회합니다."
    )
    async def get_sessions_by_user_id(
            self,
            skip: int = Query(0, description="페이지네이션: 건너뛸 항목 수", ge=0),
            limit: int = Query(10, description="페이지네이션: 한 번에 가져올 항목 수", ge=1, le=100),
            is_deleted: bool = Query(False, description="삭제된 세션 포함 여부 (true: 삭제됨, false: 활성 상태)"),
            auth: HTTPAuthorizationCredentials = Depends(security)
    ):
        user_id: str = get_user_id(auth)

        return await proxy_request(
            "GET",
            RULE_ENGINE_URL,
        f"/session/list?user_id={user_id}&skip={skip}&limit={limit}&is_deleted={is_deleted}",
            auth.credentials
        )

    # 전체 활성화 세션 목록 조회
    @state_router.get(
        "/sessions/active",
        response_model=WrappedResponse[List[SessionInfo]],
        summary="전체 활성화 세션 목록을 조회합니다.(FE에서 불필요해 보임)"
    )
    async def get_sessions(self, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await proxy_request("GET", STATE_MANAGER_URL, f"{self.base_prefix}/sessions/active", auth.credentials)


    # 세션 정보 조회
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

