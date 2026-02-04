from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_utils.cbv import cbv

from common.dtos.wrapped_response import WrappedResponse
from configs.setting import RULE_ENGINE_URL
from info.dtos.enemy_dtos import EnemyRequest, PaginatedEnemyResponse, EnemyDetailResponse
from info.dtos.item_dtos import ItemRequest, PaginatedItemResponse
from info.dtos.npc_dtos import PaginatedNpcResponse, NpcRequest, NpcDetailResponse
from info.dtos.personality_dtos import PaginatedPersonalityResponse, PersonalityRequest
from info.dtos.world_dtos import WorldInfoKey, WorldResponse
from utils.proxy_request import proxy_request

info_router = APIRouter(prefix="/info", tags=["게임 정보 중계"])
security = HTTPBearer()


@cbv(info_router)
class InfoHandler:
    base_prefix = "/info"

    # --- 1. 아이템 조회 ---
    @info_router.post(
        "/items",
        response_model=WrappedResponse[PaginatedItemResponse],
        summary="아이템 조회"
    )
    async def read_items(self, request_data: ItemRequest, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await proxy_request("POST", RULE_ENGINE_URL, f"{self.base_prefix}/items", auth.credentials, json=request_data.model_dump())

    # --- 2. 적 정보 조회 (목록) ---
    @info_router.post(
        "/enemies",
        response_model=WrappedResponse[PaginatedEnemyResponse],
        summary = "적 정보 조회(목록)"
    )
    async def read_enemies(self, request_data: EnemyRequest, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await proxy_request("POST", RULE_ENGINE_URL, f"{self.base_prefix}/enemies", auth.credentials, json=request_data.model_dump())

    @info_router.get(
        "/enemies/{enemy_id}",
        response_model=WrappedResponse[EnemyDetailResponse],
        summary="적 정보 상세 조회 - 드롭 아이템 목록 포함"
    )
    async def read_enemy_detail(self, enemy_id: int, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await proxy_request("GET", RULE_ENGINE_URL, f"{self.base_prefix}/enemies/{enemy_id}", auth.credentials)

    # --- 3. NPC 정보 조회 (목록) ---
    @info_router.post(
        "/npcs",
        response_model=WrappedResponse[PaginatedNpcResponse],
        summary="NPC 정보 조회 (목록)"
    )
    async def read_npcs(self, request_data: NpcRequest, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await proxy_request("POST", RULE_ENGINE_URL, f"{self.base_prefix}/npcs", auth.credentials, json=request_data.model_dump())

    @info_router.get(
        "/npc/{npc_id}",
        response_model=WrappedResponse[NpcDetailResponse],
        summary="NPC 정보 상세 조회 - 거래 아이템 목록 포함"
    )
    async def get_npc_detail(self, npc_id: int, auth: HTTPAuthorizationCredentials = Depends(security)):
        return await proxy_request("GET", RULE_ENGINE_URL, f"{self.base_prefix}/npc/{npc_id}", auth.credentials)

    # --- 4. 성격 정보 조회 ---
    @info_router.post(
        "/personalities",
        response_model=WrappedResponse[PaginatedPersonalityResponse],
        summary="NPC 생성 시 조합 가능한 성격 정보 조회"
    )
    async def read_personalities(self, request_data: PersonalityRequest,
                                 auth: HTTPAuthorizationCredentials = Depends(security)):
        return await proxy_request("POST", RULE_ENGINE_URL, f"{self.base_prefix}/personalities", auth.credentials, json=request_data.model_dump())

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
        return await proxy_request("GET", RULE_ENGINE_URL, f"{self.base_prefix}/world", auth.credentials, params=params)