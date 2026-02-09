from typing import Annotated, List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_utils.cbv import cbv

from configs.setting import GM_SERVICE_URL
from gm.dtos.gm_dtos import (
    GameTurnResponseV2,
    HistoryEntry,
    NpcTurnInput,
    SessionSummaryResponse,
    SummaryInput,
    UserInput,
)
from utils.proxy_request import proxy_request

gm_router = APIRouter(prefix="/gm", tags=["GM 서비스 중계"])
security = HTTPBearer()
auth_dep = Depends(security)


@cbv(gm_router)
class GmRouter:
    base_prefix = "/game"

    @gm_router.get(
        "/history/{session_id}",
        response_model=List[HistoryEntry],
        summary="게임 세션 이력을 조회합니다.",
    )
    async def get_scenario(
        self,
        session_id: str,
        auth: Annotated[HTTPAuthorizationCredentials, auth_dep],
    ):
        return await proxy_request(
            "GET",
            GM_SERVICE_URL,
            f"/api/v1{self.base_prefix}/history/{session_id}",
            auth.credentials,
        )

    @gm_router.post(
        "/turn",
        response_model=GameTurnResponseV2,
        summary="턴을 진행합니다.",
    )
    async def play_turn(
        self,
        request: UserInput,
        auth: Annotated[HTTPAuthorizationCredentials, auth_dep],
    ):
        return await proxy_request(
            "POST",
            GM_SERVICE_URL,
            f"/api/v1{self.base_prefix}/turn",
            auth.credentials,
            json=request.model_dump(),
        )

    @gm_router.post(
        "/npc-turn",
        response_model=GameTurnResponseV2,
        summary="NPC 턴을 진행합니다.",
    )
    async def play_npc_turn(
        self,
        request: NpcTurnInput,
        auth: Annotated[HTTPAuthorizationCredentials, auth_dep],
    ):
        return await proxy_request(
            "POST",
            GM_SERVICE_URL,
            f"/api/v1{self.base_prefix}/npc-turn",
            auth.credentials,
            json=request.model_dump(),
        )

    @gm_router.post(
        "/summary",
        response_model=SessionSummaryResponse,
        summary="세션 요약(나레이션 요약)을 조회합니다.",
    )
    async def get_summary(
        self,
        request: SummaryInput,
        auth: Annotated[HTTPAuthorizationCredentials, auth_dep],
    ):
        return await proxy_request(
            "POST",
            GM_SERVICE_URL,
            f"/api/v1{self.base_prefix}/summary",
            auth.credentials,
            json=request.model_dump(),
        )
