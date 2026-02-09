from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class UserInput(BaseModel):
    session_id: str = Field(..., description="세션 ID")
    content: str = Field(..., description="사용자 자연어 입력")
    # 필요한 경우 추가 메타데이터 (예: timestamp, user_id 등)
    # 현재는 최소한으로 시작


class NpcTurnInput(BaseModel):
    session_id: str = Field(..., description="세션 ID")


class SummaryInput(BaseModel):
    session_id: str = Field(..., description="세션 ID")


class TurnOutputType(str, Enum):
    npc = "npc"
    narration = "narration"


class TurnOutputKind(str, Enum):
    narration = "narration"
    dialogue = "dialogue"

class SegmentType(str, Enum):
    action = "action"
    narration = "narration"
    dialogue = "dialogue"


class Segment(BaseModel):
    type: SegmentType = Field(..., description="세그먼트 타입")
    role: str = Field(..., description="출력 주체 표시 이름(예: narrator, NPC 이름)")
    content: str = Field(..., description="세그먼트 텍스트")


class ActorType(str, Enum):
    player = "player"
    narrator = "narrator"
    npc = "npc"
    enemy = "enemy"
    unknown = "unknown"


class TurnOutput(BaseModel):
    kind: TurnOutputKind = Field(..., description="출력 종류 (나레이션/대사)")
    text: str = Field(..., description="출력 텍스트")
    actor_type: ActorType = Field(..., description="출력 주체 타입")
    actor_id: Optional[str] = Field(None, description="출력 주체 ID")
    actor_name: Optional[str] = Field(None, description="출력 주체 표시 이름")


class GameTurnResponse(BaseModel):
    turn_id: str = Field(..., description="턴 식별자")
    action: Optional[str] = Field(
        None,
        description=(
            "이번 턴의 행동(action) 원문. "
            "플레이어 턴이면 사용자 입력, NPC/적 턴이면 생성된 행동 텍스트."
        ),
    )
    narrative: str = Field(..., description="생성된 서사")
    dialogue: Optional[str] = Field(
        None,
        description=(
            "NPC/적의 직접 발화(대사). "
            "action과는 별개로 분리되어 반환된다."
        ),
    )
    outputs: List[TurnOutput] = Field(
        default_factory=list,
        description="나레이션/대사 출력 조각 리스트 (kind로 구분).",
    )
    segments: List[Segment] = Field(
        default_factory=list,
        description="구조화 출력 세그먼트 리스트 (action/dialogue/narration).",
    )
    commit_id: Optional[str] = Field(None, description="상태 확정 ID")
    active_entity_id: Optional[str] = Field(None, description="행동 엔티티 ID")
    active_entity_name: Optional[str] = Field(None, description="행동 엔티티 이름")
    output_type: TurnOutputType = Field(..., description="출력 주체 타입")
    is_npc_turn: bool = Field(False, description="NPC 턴 여부")
    npc_turn: Optional["GameTurnResponse"] = Field(None, description="연쇄 NPC 턴")


class GameTurnResponseV2(BaseModel):
    """
    Segments-only 응답 모델 (레거시 narrative/dialogue/outputs 제거).
    """

    turn_id: str = Field(..., description="턴 식별자")
    commit_id: Optional[str] = Field(None, description="상태 확정 ID")
    active_entity_id: Optional[str] = Field(None, description="행동 엔티티 ID")
    active_entity_name: Optional[str] = Field(None, description="행동 엔티티 이름")
    is_npc_turn: bool = Field(False, description="NPC 턴 여부")
    current_act_id: Optional[str] = Field(None, description="턴 이후 현재 ACT ID")
    current_sequence_id: Optional[str] = Field(None, description="턴 이후 현재 시퀀스 ID")
    session_status: Optional[str] = Field(None, description="턴 이후 세션 status (active/ended 등)")
    is_session_ended: bool = Field(False, description="턴 이후 세션 종료 여부")
    segments: List[Segment] = Field(
        default_factory=list,
        description="구조화 출력 세그먼트 리스트 (action/dialogue/narration).",
    )
    transition: Optional[dict] = Field(
        None,
        description=(
            "ACT/SEQUENCE 전이 정보. "
            "예: {from_act_id, from_sequence_id, to_act_id, to_sequence_id, changed}."
        ),
    )
    npc_turn: Optional["GameTurnResponseV2"] = Field(None, description="연쇄 NPC 턴")


class SessionSummaryResponse(BaseModel):
    session_id: str = Field(..., description="세션 ID")
    summary: str = Field(..., description="세션 요약")


class HistoryEntry(BaseModel):
    session_id: str = Field(..., description="세션 ID")
    act_id: Optional[str] = Field(None, description="ACT ID")
    sequence_id: Optional[str] = Field(None, description="시퀀스 ID")
    sequence_type: Optional[str] = Field(None, description="시퀀스 타입")
    sequence_seq: Optional[int] = Field(None, description="시퀀스 순번")
    turn_seq: int = Field(..., description="턴 순번")
    active_entity_id: Optional[str] = Field(None, description="행동 엔티티 ID")
    user_input: Optional[str] = Field(None, description="입력 텍스트")
    narrative: str = Field(..., description="서사 텍스트")
    created_at: Optional[str] = Field(None, description="생성 시각")
