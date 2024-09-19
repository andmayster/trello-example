from enum import Enum


class ControllerEntities(str, Enum):
    users = "users"
    boards = "boards"
    tasks = "tasks"
    lists = "lists"
    comments = "comments"
    tags = "tags"