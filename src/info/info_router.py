import httpx
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_utils.cbv import cbv

from common.dtos.wrapped_response import WrappedResponse
from configs.setting import REMOTE_SERVICE_URL
from info.dtos.enemy_dtos import EnemyRequest, PaginatedEnemyResponse, EnemyDetailResponse
from info.dtos.npc_dtos import PaginatedNpcResponse, NpcRequest, NpcDetailResponse
from info.dtos.personality_dtos import PaginatedPersonalityResponse, PersonalityRequest
from info.dtos.world_dtos import WorldInfoKey, WorldResponse
from info.dtos.item_dtos import ItemRequest, PaginatedItemResponse

info_router = APIRouter(prefix="/info", tags=["게임 정보 중계"])
security = HTTPBearer()


@cbv(info_router)
class InfoHandler:

    async def _proxy_request(self, method: str, path: str, token: str, params=None, json=None):
        """마이크로서비스로 요청을 전달하는 공통 비동기 메서드"""
        async with httpx.AsyncClient() as client:
            try:
                url = f"{REMOTE_SERVICE_URL}{path}"
                headers = {"Authorization": f"Bearer {token}"}

                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json,
                    timeout=10.0
                )

                if response.status_code >= 400:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=response.json().get("detail", "Remote Service Error")
                    )
                return response.json()

            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"마이크로서비스 연결 실패: {exc}"
                )

    # --- 1. 아이템 조회 ---
    @info_router.post(
        "/items",
        response_model=WrappedResponse[PaginatedItemResponse],
        summary="아이템 조회"
    )
    async def read_items(self, request_data: ItemRequest, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await self._proxy_request("POST", "/items", auth.credentials, json=request_data.dict())

    # --- 2. 적 정보 조회 (목록) ---
    @info_router.post(
        "/enemies",
        response_model=WrappedResponse[PaginatedEnemyResponse],
        summary = "적 정보 조회(목록)"
    )
    async def read_enemies(self, request_data: EnemyRequest, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await self._proxy_request("POST", "/enemies", auth.credentials, json=request_data.dict())

    @info_router.get(
        "/enemies/{enemy_id}",
        response_model=WrappedResponse[EnemyDetailResponse],
        summary="적 정보 상세 조회 - 드롭 아이템 목록 포함"
    )
    async def read_enemy_detail(self, enemy_id: int, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await self._proxy_request("GET", f"/enemies/{enemy_id}", auth.credentials)

    # --- 3. NPC 정보 조회 (목록) ---
    @info_router.post(
        "/npcs",
        response_model=WrappedResponse[PaginatedNpcResponse],
        summary="NPC 정보 조회 (목록)"
    )
    async def read_npcs(self, request_data: NpcRequest, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await self._proxy_request("POST", "/npcs", auth.credentials, json=request_data.dict())

    @info_router.get(
        "/npc/{npc_id}",
        response_model=WrappedResponse[NpcDetailResponse],
        summary="NPC 정보 상세 조회 - 거래 아이템 목록 포함"
    )
    async def get_npc_detail(self, npc_id: int, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await self._proxy_request("GET", f"/npc/{npc_id}", auth.credentials)

    # --- 4. 성격 정보 조회 ---
    @info_router.post(
        "/personalities",
        response_model=WrappedResponse[PaginatedPersonalityResponse],
        summary="NPC 생성 시 조합 가능한 성격 정보 조회"
    )
    async def read_personalities(self, request_data: PersonalityRequest,
                                 auth: HTTPAuthorizationCredentials = Depends(security)):
        return await self._proxy_request("POST", "/personalities", auth.credentials, json=request_data.dict())

    # --- 5. 월드 정보 조회 (GET Query Params) ---
    @info_router.get(
        "/world",
        response_model=WrappedResponse[WorldResponse],
        summary="월드 정보 조회 (GET Query Params)"
    )
    async def read_world(
            self,
            include_keys: Optional[List[WorldInfoKey]] = Query(None),
            auth: HTTPAuthorizationCredentials = Depends(security)
    ):
        params = [("include_keys", k.value) for k in include_keys] if include_keys else None
        return await self._proxy_request("GET", "/world", auth.credentials, params=params)