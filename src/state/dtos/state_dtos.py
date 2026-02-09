from datetime import datetime
from typing import Annotated, Any, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from common.dtos.pagination_meta import PaginationMeta
from src.utils.parse_json import parse_json


class NPCRelation(BaseModel):
    npc_id: Union[str, UUID]
    npc_name: Optional[str] = None
    affinity_score: int
    model_config = ConfigDict(from_attributes=True)


class ItemBase(BaseModel):
    item_id: str
    name: str
    description: str = ""
    item_type: str = "misc"
    meta: dict[str, Any] = Field(default_factory=dict)
    is_stackable: bool = True


class PlayerStateResponse(BaseModel):
    hp: int
    gold: int
    items: List[ItemBase] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)

class FullPlayerState(BaseModel):
    player: PlayerStateResponse
    player_npc_relations: List[NPCRelation]
    model_config = ConfigDict(from_attributes=True)

class ScenarioInfo(BaseModel):
    """조회용 정보"""

    scenario_id: Union[str, UUID]
    title: str
    description: Optional[str] = None
    difficulty: Optional[str] = None
    genre: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    acts: List[dict[str, Any]] = Field(default_factory=list)
    sequences: List[dict[str, Any]] = Field(default_factory=list)
    npcs: List[dict[str, Any]] = Field(default_factory=list)
    enemies: List[dict[str, Any]] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class SessionStartRequest(BaseModel):
    """세션 시작 요청"""

    scenario_id: str = Field(..., description="시나리오 UUID")
    current_act: int = Field(default=1, description="시작 Act", ge=1)
    current_sequence: int = Field(default=1, description="시작 Sequence", ge=1)
    location: str = Field(default="Starting Town", description="시작 위치")
    # user_id: Optional[int] = Field(default=None, description="외부 시스템 사용자 ID")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "scenario_id": "550e8400-e29b-41d4-a716-446655440000",
                "current_act": 1,
                "current_sequence": 1,
                "location": "Starting Town",
            }
        }
    )


class InventoryUpdateRequest(BaseModel):
    """세션 시작 직후 스타터 아이템 지급 등에 사용하는 인벤토리 업데이트 요청"""

    player_id: str = Field(..., description="플레이어 UUID")
    rule_id: int = Field(..., description="아이템 Rule ID")
    quantity: int = Field(..., description="수량 변화량")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "player_id": "ed0234e3-ac5a-49ab-adc2-bab72f01953d",
                "rule_id": 7901,
                "quantity": 1,
            }
        }
    )


class ItemEarnRequest(BaseModel):
    """플레이어 아이템 획득 요청 (state-manager /state/player/item/earn 중계용)"""

    session_id: str = Field(..., description="세션 UUID")
    player_id: str = Field(..., description="플레이어 UUID")
    item_id: str = Field(..., description="아이템 상태 엔티티 UUID")
    rule_id: int | None = Field(default=None, description="아이템 Rule ID (optional)")
    quantity: int = Field(..., description="획득 수량")


class ItemUseRequest(BaseModel):
    """플레이어 아이템 사용 요청 (state-manager /state/player/item/use 중계용)"""

    session_id: str = Field(..., description="세션 UUID")
    player_id: str = Field(..., description="플레이어 UUID")
    item_id: str = Field(..., description="아이템 상태 엔티티 UUID")
    rule_id: int | None = Field(default=None, description="아이템 Rule ID (optional)")
    quantity: int = Field(..., description="사용 수량")


class SessionInfo(BaseModel):
    session_id: Union[str, UUID]
    scenario_id: Union[str, UUID]
    user_id: Optional[int] = None  # 외부 시스템 사용자 식별자 (Optional)
    player_id: Optional[Union[str, UUID]] = None

    # 숫자 카운터
    current_act: int
    current_sequence: int

    # 문자열 ID (신규)
    current_act_id: Optional[str] = "act-1"
    current_sequence_id: Optional[str] = "seq-1"

    current_phase: str = "exploration"
    current_turn: int = 1
    location: Optional[str] = None
    status: str
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

JsonField = Annotated[Any, BeforeValidator(parse_json)]

class SequenceEntityInfo(BaseModel):
    """시퀀스 내 엔티티 요약 정보"""

    id: Union[str, UUID]
    scenario_entity_id: str  # scenario_npc_id or scenario_enemy_id
    name: str
    description: Optional[str] = None
    entity_type: str  # 'npc' or 'enemy'
    tags: JsonField = []
    state: JsonField = None
    is_defeated: Optional[bool] = None  # enemy only

    model_config = ConfigDict(from_attributes=True)

class EntityRelationInfo(BaseModel):
    """엔티티 간 관계 정보 (Apache AGE 그래프 RELATION 엣지)"""

    from_id: str  # scenario_npc_id or scenario_enemy_id
    from_name: str
    to_id: str
    to_name: str
    relation_type: str
    affinity: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class PlayerNPCRelationInfo(BaseModel):
    """플레이어-NPC 호감도 관계"""

    npc_id: Union[str, UUID]
    npc_name: str
    scenario_npc_id: str
    affinity_score: int
    relation_type: str
    interaction_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class SequenceItemInfo(BaseModel):
    """시퀀스 내 아이템 요약 정보"""

    item_id: Union[str, UUID]
    scenario_item_id: str
    name: str
    description: Optional[str] = None
    item_type: Optional[str] = None
    meta: JsonField = {}

    model_config = ConfigDict(from_attributes=True)


class SequenceDetailInfo(BaseModel):
    """시퀀스 상세 정보 (엔티티 및 관계 포함)"""

    # 시퀀스 기본 정보
    scenario_id: Union[str, UUID]
    sequence_id: str
    sequence_name: str
    location_name: Optional[str] = None
    description: Optional[str] = None
    goal: Optional[str] = None
    exit_triggers: JsonField = []
    metadata: JsonField = {}
    # 시퀀스 내 엔티티
    npcs: List[SequenceEntityInfo] = []
    enemies: List[SequenceEntityInfo] = []
    items: List[SequenceItemInfo] = []
    # 엔티티 간 관계 (NPC-NPC, NPC-Enemy 등)
    entity_relations: List[EntityRelationInfo] = []
    # 플레이어-NPC 호감도 관계
    player_npc_relations: List[PlayerNPCRelationInfo] = []

    model_config = ConfigDict(from_attributes=True)


class SessionResponse(BaseModel):
    user_id: int
    session_id: str
    created_at: datetime

class PaginatedSessionResponse(BaseModel):
    sessions: List[SessionResponse]
    meta: PaginationMeta
