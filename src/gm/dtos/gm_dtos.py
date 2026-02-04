from pydantic import BaseModel, Field

class UserInput(BaseModel):
    session_id: str = Field(..., description="세션 ID")
    content: str = Field(..., description="사용자 자연어 입력")
    # 필요한 경우 추가 메타데이터 (예: timestamp, user_id 등)
    # 현재는 최소한으로 시작