from core.models import Task
from crud.base import BaseCRUD


class TaskCRUD(BaseCRUD):
    model = Task
