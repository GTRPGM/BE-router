from info.info_router import info_router
from src.auth.auth_router import auth_router

API_ROUTERS = [
    auth_router,
    info_router,
]
