import httpx

from configs.setting import REMOTE_SERVICE_URL, REMOTE_HOST, RULE_ENGINE_PORT
from fastapi import HTTPException


async def proxy_stream(path: str, token: str, params=None):
    """마이크로서비스의 스트리밍 응답을 중계하는 메서드"""
    url = f"http://{REMOTE_HOST}:{RULE_ENGINE_PORT}{path}"
    headers = {"Authorization": f"Bearer {token}"}

    # AsyncClient를 context manager로 열어 연결 유지
    client = httpx.AsyncClient()

    try:
        # 1. 원격 서버로 스트림 요청 시작
        # generator 함수를 정의하여 StreamingResponse에 전달
        async def stream_generator():
            try:
                async with client.stream("GET", url, headers=headers, params=params, timeout=None) as response:
                    if response.status_code >= 400:
                        # 에러 발생 시 에러 메시지 한 번 출력 후 종료
                        yield f"data: Error {response.status_code}\n\n".encode()
                        return

                    async for chunk in response.aiter_bytes():
                        yield chunk
            finally:
                await client.aclose()  # 모든 스트리밍 종료 후 클라이언트 닫기

        return stream_generator()

    except Exception as exc:
        await client.aclose()
        raise HTTPException(status_code=503, detail=f"스트리밍 연결 실패: {exc}")