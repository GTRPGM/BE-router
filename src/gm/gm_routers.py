from typing import List, Dict, Any

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_utils.cbv import cbv

from common.dtos.wrapped_response import WrappedResponse
from configs.setting import GM_SERVICE_URL
from gm.dtos.gm_dtos import UserInput
from utils.proxy_request import proxy_request

gm_router = APIRouter(prefix="/gm", tags=["GM 서비스 중계"])
security = HTTPBearer()

@cbv(gm_router)
class GmRouter:
    base_prefix = "/game"

    @gm_router.get(
        "/history/{session_id}",
        response_model=List[Dict[str, Any]],
        summary="게임 세션 이력을 조회합니다."
    )
    async def get_scenario(self, session_id: str, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await proxy_request("GET", GM_SERVICE_URL, f"/api/v1{self.base_prefix}/history/{session_id}", auth.credentials)

    @gm_router.post(
        "/turn",
        # response_model=WrappedResponse[Any],
        summary="턴을 진행합니다."
    )
    async def play_turn(self, request: UserInput, auth: HTTPAuthorizationCredentials = Depends(security)):
        print(GM_SERVICE_URL)
        print(f"/api/v1{self.base_prefix}/turn")
        return await proxy_request("POST", GM_SERVICE_URL, f"/api/v1{self.base_prefix}/turn", auth.credentials, json=request.model_dump())