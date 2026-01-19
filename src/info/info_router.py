from fastapi import APIRouter, Query, Depends
from fastapi_utils.cbv import cbv
from typing import List, Optional

from common.dtos.wrapped_response import WrappedResponse
from common.utils.get_services import get_item_service
from info import item_service
from info.dtos.item_dtos import PaginatedItemResponse
from info.item_service import ItemService

info_router = APIRouter(prefix="/info", tags=["게임 정보 조회"])

@cbv(info_router)
class InfoHandler:
    @info_router.get(
        "/items",
        summary="아이템 목록 조회",
        response_model=WrappedResponse[PaginatedItemResponse],
    )
    async def read_items(
            self,
            item_ids: Optional[List[int]] = Query(None, description="필터링할 아이템 ID 리스트"),
            skip: int = Query(0, ge=0),
            limit: int = Query(20, ge=1, le=100),
            item_service: ItemService = Depends(get_item_service)
    ):
        # 서비스 계층 호출 (실제 구현 시 의존성 주입된 인스턴스 사용)
        items, meta = await item_service.get_items(item_ids, skip, limit)

        return {
            "data": {
                "items": items,
                "meta": meta
            }
        }