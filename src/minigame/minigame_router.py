from fastapi import APIRouter
from fastapi_utils.cbv import cbv
import httpx
from starlette.responses import StreamingResponse

from configs.setting import RULE_ENGINE_PORT, REMOTE_HOST

minigame_router = APIRouter(prefix="/minigame", tags=["미니게임 - 수수께끼"])

@cbv(minigame_router)
class MinigameRouter:
    @minigame_router.get(
        "/minigame",
        summary="GM과 수수께끼 미니게임을 진행합니다."
    )
    async def proxy_riddle(self):
        async def stream_generator():
            async with httpx.AsyncClient() as client:
                async with client.stream("GET", f"http://{REMOTE_HOST}:{RULE_ENGINE_PORT}/minigame") as response:
                    # 데이터가 들어오는 대로 프론트로 yield
                    async for chunk in response.aiter_bytes():
                        yield chunk

        return StreamingResponse(stream_generator(), media_type="text/event-stream")
