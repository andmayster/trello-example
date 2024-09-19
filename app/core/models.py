from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, func, TIMESTAMP, Enum
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import relationship, declarative_base

from core.settings import settings


Base = declarative_base()
engine = create_async_engine(settings.DATABASE_URL)

task_tags = Table(
    'task_tags',
    Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)


class TaskStatus(PyEnum):
    TODO = "TODO"
    IN_PROGRESS = "In progress"
    DONE = "Done"

class TaskPriority(PyEnum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)
    hash_password = Column(String)
    role_id = Column(Integer, ForeignKey('roles.id'))

    tasks_created = relationship("Task", back_populates="creator", overlaps="assignees,tasks_assigned")
    tasks_assigned = relationship("Task", back_populates="assignees", overlaps="creator,tasks_created")

    boards = relationship("Board", back_populates="owner")  # Один пользователь может иметь несколько досок
    role = relationship("Role", back_populates="users")


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(Text)
    users = relationship("User", back_populates="role")


class Board(Base):
    __tablename__ = 'boards'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="boards")  # Один владелец может иметь несколько досок
    lists = relationship("TaskList", back_populates="board", cascade="all, delete-orphan")


class TaskList(Base):
    __tablename__ = 'lists'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    board_id = Column(Integer, ForeignKey('boards.id'))
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    board = relationship("Board", back_populates="lists")  # Один список принадлежит одной доске
    tasks = relationship(
        "Task", back_populates="task_list",
        cascade="all, delete-orphan"
    )  # Список может содержать несколько задач


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    responsible_user_id = Column(Integer, ForeignKey('users.id'))
    task_list_id = Column(Integer, ForeignKey('lists.id'))  # Ссылка на колонку (список)
    task_list = relationship("TaskList", back_populates="tasks")  # Одна колонка содержит несколько задач
    creator = relationship("User", back_populates="tasks_created", foreign_keys=[responsible_user_id], overlaps="assignees,tasks_assigned")
    assignees = relationship("User", back_populates="tasks_assigned", foreign_keys=[responsible_user_id], overlaps="creator,task_created")
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)

    # Связь с комментариями
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")

    # Связь с тегами
    tags = relationship("Tag", secondary=task_tags, back_populates="tasks")

    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())

    task = relationship("Task", back_populates="comments")  # Один комментарий принадлежит одной задаче
    user = relationship("User")


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    color = Column(String)

    tasks = relationship("Task", secondary="task_tags", back_populates="tags")
