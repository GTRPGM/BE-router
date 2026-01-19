from pydantic import BaseModel, Field
from typing import List, Optional

from common.dtos.pagination_meta import PaginationMeta


class ItemResponse(BaseModel):
    item_id: int
    name: str
    type: str
    effect_value: int
    description: Optional[str]
    weight: int
    grade: Optional[str]
    base_price: int

class PaginatedItemResponse(BaseModel):
    items: List[ItemResponse]
    meta: PaginationMeta