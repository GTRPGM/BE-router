from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_utils.cbv import cbv

from configs.setting import SCENARIO_SERVICE_URL
from utils.proxy_request import proxy_request

scenario_router = APIRouter(prefix="/scenario", tags=["시나리오 서비스 중계"])
security = HTTPBearer()
auth_dep = Depends(security)


@cbv(scenario_router)
class ScenarioRouter:
    @scenario_router.post(
        "/generation/pure",
        summary="시나리오 생성(Pure)",
    )
    async def generate_pure(
        self,
        payload: dict[str, Any],
        auth: Annotated[HTTPAuthorizationCredentials, auth_dep],
    ):
        return await proxy_request(
            "POST",
            SCENARIO_SERVICE_URL,
            "/api/v1/generation/pure",
            auth.credentials,
            json=payload,
        )

    @scenario_router.post(
        "/manage/scenarios/{scenario_id}/inject",
        summary="시나리오 주입",
    )
    async def inject_scenario(
        self,
        scenario_id: str,
        auth: Annotated[HTTPAuthorizationCredentials, auth_dep],
    ):
        return await proxy_request(
            "POST",
            SCENARIO_SERVICE_URL,
            f"/api/v1/manage/scenarios/{scenario_id}/inject",
            auth.credentials,
        )
