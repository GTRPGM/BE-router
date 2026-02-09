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
    narrative: str = Field(..., description="생성된 서사")
    dialogue: Optional[str] = Field(
        None,
        description=(
            "NPC/적의 직접 발화(대사). "
            "행동(action)은 응답 필드로 노출하지 않고 나레이션 생성 입력으로만 사용한다."
        ),
    )
    outputs: List[TurnOutput] = Field(
        default_factory=list,
        description="나레이션/대사 출력 조각 리스트 (kind로 구분).",
    )
    commit_id: Optional[str] = Field(None, description="상태 확정 ID")
    active_entity_id: Optional[str] = Field(None, description="행동 엔티티 ID")
    active_entity_name: Optional[str] = Field(None, description="행동 엔티티 이름")
    output_type: TurnOutputType = Field(..., description="출력 주체 타입")
    is_npc_turn: bool = Field(False, description="NPC 턴 여부")
    npc_turn: Optional["GameTurnResponse"] = Field(None, description="연쇄 NPC 턴")


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
