import httpx

from configs.database import check_db_connection
from configs.http_client import http_holder
from configs.redis_conn import check_redis_connection
from configs.setting import APP_PORT
from utils.logger import info


def _initialize_http_client():
    info("HTTP 클라이언트를 구성합니다...")
    http_holder.client = httpx.AsyncClient(
        timeout=httpx.Timeout(10.0), limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
    )


def _print_startup_message():
    print("\n" + "⭐" * 40)
    print(f"  Swagger UI: http://127.0.0.1:{APP_PORT}/docs")
    print(f"  ReDoc:      http://127.0.0.1:{APP_PORT}/redoc")
    print("⭐" * 40 + "\n")


def startup_event_handler():
    check_db_connection()
    check_redis_connection()
    _initialize_http_client()
    _print_startup_message()


async def shutdown_event_handler():
    await http_holder.client.aclose()
    info("HTTP 클라이언트 종료 중...")
    info("BE router 종료 중...")
