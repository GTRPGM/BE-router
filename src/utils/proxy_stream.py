import httpx
from fastapi import HTTPException

from configs.http_client import http_holder


async def proxy_stream(base_url: str, path: str, token: str, params=None):
    """마이크로서비스의 스트리밍 응답을 중계하는 메서드"""
    url = f"{base_url}{path}"
    headers = {"Authorization": f"Bearer {token}"}

    client = http_holder.client
    if not client:
        raise HTTPException(status_code=503, detail="HTTP 클라이언트가 준비되지 않았습니다.")

    # 스트림 전용 제너레이터 정의
    async def stream_generator():
        try:
            # 공용 클라이언트의 .stream()을 사용 (timeout=None은 스트리밍 유지용)
            async with client.stream("GET", url, headers=headers, params=params, timeout=None) as response:
                if response.status_code >= 400:
                    yield f"연결 오류 {response.status_code}".encode()
                    return

                async for chunk in response.aiter_bytes():
                    yield chunk
        except httpx.RequestError as exc:
            yield f"네트워크 오류: {str(exc)}".encode()

    return stream_generator()