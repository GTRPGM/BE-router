from fastapi import HTTPException, status
from configs.http_client import http_holder
from configs.setting import LLM_GATEWAY_URL
from utils.logger import error

async def get_game_tip_sentence() -> str:
    """
    LLM을 호출하여 타자 연습용 게임 팁 문장을 가져옵니다.
    """
    if not http_holder.client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="HTTP Client not initialized",
        )

    user_prompt = "타자 연습으로 사용하기 좋은 TRPG에 관한 짧은 게임 팁을 하나 알려줘. 한국어로 한 문장이어야 해."

    payload = {
        "model": "gemini-2.5-flash",
        "messages": [
            {
            "role": "system",
            "content": user_prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000,
        "stream": False
        }

    try:
        response = await http_holder.client.post(
            f"{LLM_GATEWAY_URL}/api/v1/chat/completions",
            json=payload,
            timeout=30.0,
        )
        response.raise_for_status()

        data = response.json()
        # Chat Completion API 응답 구조에서 팁 추출
        tip = data.get("choices")[0].get("message").get("content")

        if not tip:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="LLM으로부터 유효한 응답을 받지 못했습니다.",
            )

        return tip

    except HTTPException as e:
        raise e
    except Exception as e:
        error(f"LLM Gateway 호출 중 에러 발생: {e}")
        if response and response.text:
            error(f"LLM Gateway로부터 받은 전체 응답: {response.text}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="LLM 서비스 호출에 실패했습니다. 자세한 내용은 서버 로그를 확인하세요.",
        )

