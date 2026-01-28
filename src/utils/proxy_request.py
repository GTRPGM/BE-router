import httpx

from fastapi import HTTPException, status


async def proxy_request(method: str, base_url: str, path: str, token: str, params=None, json=None):
    """마이크로서비스로 요청을 전달하는 공통 비동기 메서드"""
    async with httpx.AsyncClient() as client:
        try:
            url = f"{base_url}{path}"
            headers = {"Authorization": f"Bearer {token}"}

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
                    detail=response.json().get("detail", "Remote Service Error")
                )
            return response.json()

        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"마이크로서비스 연결 실패: {exc}"
            )