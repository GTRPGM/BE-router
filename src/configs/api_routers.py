from src.user.user_router import user_router
from src.auth.auth_router import auth_router
from src.state.state_router import state_router
from src.gm.gm_routers import gm_router
from info.info_router import info_router
from src.minigame.minigame_router import minigame_router

API_ROUTERS = [
    user_router,
    auth_router,
    state_router,
    gm_router,
    info_router,
    minigame_router
]
