import asyncio
import os

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

os.environ.setdefault("APP_PORT", "8010")
os.environ.setdefault("GM_PORT", "8020")
os.environ.setdefault("REMOTE_HOST", "localhost")

from gm.dtos.gm_dtos import UserInput
from gm.gm_routers import GmRouter
from utils import proxy_request as proxy_module


class _MockResponse:
    def __init__(self, status_code: int, body):
        self.status_code = status_code
        self._body = body
        self.text = body if isinstance(body, str) else ""

    def json(self):
        if isinstance(self._body, Exception):
            raise self._body
        return self._body


def test_proxy_request_forwards_auth_and_payload():
    captured = {}

    class _Client:
        async def request(self, **kwargs):
            captured.update(kwargs)
            return _MockResponse(200, {"ok": True})

    proxy_module.http_holder.client = _Client()
    result = asyncio.run(
        proxy_module.proxy_request(
            method="POST",
            base_url="http://gm:8020",
            path="/api/v1/game/turn",
            token="token-123",
            json={"session_id": "s1", "content": "hello"},
        )
    )

    assert result == {"ok": True}
    assert captured["url"] == "http://gm:8020/api/v1/game/turn"
    assert captured["headers"]["Authorization"] == "Bearer token-123"
    assert captured["json"]["session_id"] == "s1"


def test_proxy_request_preserves_upstream_error_detail():
    class _Client:
        async def request(self, **kwargs):
            return _MockResponse(422, {"detail": "invalid payload"})

    proxy_module.http_holder.client = _Client()
    with pytest.raises(HTTPException) as exc:
        asyncio.run(
            proxy_module.proxy_request(
                method="POST",
                base_url="http://gm:8020",
                path="/api/v1/game/turn",
                token="token-123",
                json={"bad": True},
            )
        )
    assert exc.value.status_code == 422
    assert exc.value.detail == "invalid payload"


def test_gm_router_turn_keeps_payload_shape(monkeypatch):
    router = GmRouter()
    auth = HTTPAuthorizationCredentials(scheme="Bearer", credentials="jwt")
    req = UserInput(session_id="s1", content="do something")
    called = {}

    async def _fake_proxy(method, base_url, path, token=None, params=None, json=None):
        called.update(
            {
                "method": method,
                "base_url": base_url,
                "path": path,
                "token": token,
                "json": json,
            }
        )
        return {"ok": True}

    monkeypatch.setattr("gm.gm_routers.proxy_request", _fake_proxy)
    out = asyncio.run(router.play_turn(req, auth))

    assert out == {"ok": True}
    assert called["method"] == "POST"
    assert called["path"] == "/api/v1/game/turn"
    assert called["json"] == {"session_id": "s1", "content": "do something"}
