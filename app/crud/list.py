from core.models import TaskList
from crud.base import BaseCRUD


class TaskListCRUD(BaseCRUD):
    model = TaskList
