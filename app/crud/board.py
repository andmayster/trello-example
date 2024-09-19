from core.models import Board
from crud.base import BaseCRUD


class BoardCRUD(BaseCRUD):
    model = Board
