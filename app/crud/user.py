from core.models import User
from crud.base import BaseCRUD


class UserCRUD(BaseCRUD):
    model = User
