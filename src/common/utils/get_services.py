from fastapi.params import Depends

from auth.auth_service import AuthService
from configs.database import get_db_cursor
from info.item_service import ItemService


def get_auth_service(cursor = Depends(get_db_cursor)):
    return AuthService(cursor)

def get_item_service(cursor = Depends(get_db_cursor)):
    return ItemService(cursor)