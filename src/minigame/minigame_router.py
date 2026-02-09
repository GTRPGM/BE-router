from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_utils.cbv import cbv
from jose import jwt
from starlette.responses import StreamingResponse

from configs.setting import ALGORITHM, RULE_ENGINE_URL, SECRET_KEY
from minigame.dtos.minigame_dtos import AnswerRequest
from utils.proxy_request import proxy_request
from utils.proxy_stream import proxy_stream

minigame_router = APIRouter(prefix="/minigame", tags=["미니게임"])
auth_scheme = HTTPBearer()


@cbv(minigame_router)
class MinigameRouter:
    base_prefix = "/play"

    @minigame_router.get("/riddle", summary="GM과 수수께끼 미니게임을 진행합니다.")
    async def proxy_riddle(
        self,
        token_auth: HTTPAuthorizationCredentials = Depends(auth_scheme),
    ):
        # 1. 토큰에서 user_id 추출 (이미 구현된 토큰 디코딩 함수가 있다고 가정)
        token = token_auth.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # 2. rule-engine 마이크로서비스 엔드포인트 호출
        user_id: str = payload.get("sub")
        path = f"{self.base_prefix}/riddle/{user_id}"

        # 3. 스트리밍 중계 실행
        generator = await proxy_stream(RULE_ENGINE_URL, path, token)

        return StreamingResponse(generator, media_type="text/event-stream")

    @minigame_router.get("/quiz", summary="GM과 동굴 탐험대 퀴즈 미니게임을 진행합니다.")
    async def proxy_quiz(
        self,
        token_auth: HTTPAuthorizationCredentials = Depends(auth_scheme),
    ):
        # 1. 토큰에서 user_id 추출 (이미 구현된 토큰 디코딩 함수가 있다고 가정)
        token = token_auth.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # 2. rule-engine 마이크로서비스 엔드포인트 호출
        user_id: str = payload.get("sub")
        path = f"{self.base_prefix}/quiz/{user_id}"

        # 3. 스트리밍 중계 실행
        generator = await proxy_stream(RULE_ENGINE_URL, path, token)

        return StreamingResponse(generator, media_type="text/event-stream")

    @minigame_router.post("/answer", summary="사용자가 입력한 답안의 정답 여부를 확인합니다.")
    async def proxy_answer(
        self,
        request: AnswerRequest,
        token_auth: HTTPAuthorizationCredentials = Depends(auth_scheme),
    ):
        # 1. 토큰에서 유저 정보 추출
        token = token_auth.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        # 2. rule-engine 마이크로서비스 경로 설정
        path = f"{self.base_prefix}/answer/{user_id}"

        # 3. proxy_request를 통해 rule-engine 마이크로서비스로 요청 전달
        response_data = await proxy_request(
            method="POST", base_url=RULE_ENGINE_URL, path=path, token=token, json=request.model_dump()
        )

        return response_data
