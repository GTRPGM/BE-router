import httpx
from configs.http_client import http_holder
from fastapi import HTTPException, status


async def proxy_request(method: str, base_url: str, path: str, token: str = None, params=None, json=None):
    """마이크로서비스로 요청을 전달하는 공통 비동기 메서드"""
    url = f"{base_url}{path}"
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    client = http_holder.client
    if not client:
        raise HTTPException(status_code=503, detail="HTTP 클라이언트가 준비되지 않았습니다.")

    try:
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=json,
            timeout=10.0
        )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "원격 서비스 오류"),
            )
        return response.json()

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"마이크로서비스 연결 실패: {exc}"
        )