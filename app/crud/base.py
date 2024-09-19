import typing
from abc import ABCMeta
from contextlib import asynccontextmanager
from typing import TypeVar, AsyncGenerator
from uuid import UUID

from fastapi_async_sqlalchemy import db
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.models import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseCRUD(metaclass=ABCMeta):
    model: ModelType  # type: ignore

    @classmethod
    async def create(
        cls,
        params: dict[str, typing.Any],
        commit: bool = True,
        autoflush: bool = False,
    ) -> ModelType:
        obj = cls.model(**params)  # type: ignore
        db.session.add(obj)

        if commit:
            await db.session.commit()
            await db.session.refresh(obj)

        if autoflush:
            await db.session.flush()

        return obj

    @classmethod
    async def bulk_create(
            cls,
            items: typing.List[dict[str, typing.Any]],
            commit: bool = True,
    ):
        # Проверяем, является ли `cls.model` объектом `Table`
        if isinstance(cls.model, Table):
            # Формируем запросы вставки для объекта `Table`
            insert_statements = [cls.model.insert().values(**params) for params in items]
            for statement in insert_statements:
                await db.session.execute(statement)
        else:
            # Текущая логика для классов моделей
            objects = [cls.model(**params) for params in items]
            db.session.add_all(objects)

        if commit:
            await db.session.commit()

        # Возвращаем объекты или None, так как для `Table` нельзя получить объекты напрямую
        return objects if not isinstance(cls.model, Table) else None

    @classmethod
    @asynccontextmanager
    async def transaction(cls) -> AsyncGenerator[AsyncSession, None]:
        async with db.session as session:
            yield session

    @classmethod
    async def get(cls, *args, **kwargs) -> ModelType:  # retrieve method
        result = await db.session.execute(
            select(cls.model).filter(*args).filter_by(**kwargs)
        )
        return result.scalars().first()

    @classmethod
    async def update(
        cls,
        record_id: int | None,
        params: dict[str, typing.Any],
        commit: bool = True,
        autoflush: bool = False,
    ) -> ModelType | None:
        if record_id is None:
            raise ValueError("id is None")

        obj = await cls.get(id=record_id)
        if obj:
            for param in params:
                setattr(obj, param, params[param])

            if commit:
                await db.session.commit()
                await db.session.refresh(obj)

            if autoflush:
                await db.session.flush()

            return obj
        return None

    @classmethod
    async def filter(cls, *args, **kwargs) -> typing.Sequence[ModelType]:
        statement = select(cls.model).filter(*args).filter_by(**kwargs)
        result = await db.session.execute(statement)
        return result.scalars().all()

    @classmethod
    async def filter_limits(
            cls,
            *args,
            limit: int = None,
            offset: int = None,
            order_by: typing.Literal["asc", "desc"] = None,
            **kwargs
    ) -> typing.List[Base]:
        statement = select(cls.model)

        if args:
            statement = statement.filter(*args)
        if kwargs:
            statement = statement.filter_by(**kwargs)

        if limit is not None:
            statement = statement.limit(limit)
        if offset is not None:
            statement = statement.offset(offset)

        if order_by is not None:
            if order_by == "asc":
                statement = statement.order_by(cls.model.created_at.asc())
            elif order_by == "desc":
                statement = statement.order_by(cls.model.created_at.desc())

        result = await db.session.execute(statement)
        return result.scalars().all()

    @classmethod
    async def delete(
        cls, record_id: int, commit: bool = True, autoflush: bool = False
    ) -> bool | None:
        obj = await cls.get(id=record_id)
        if obj:
            if autoflush:
                await db.session.flush()

            if commit:
                await db.session.delete(obj)
                await db.session.commit()

            return True
        return False

    @classmethod
    async def get_by_ids(cls, ids: list[int]) -> typing.Sequence[ModelType]:
        statement = select(cls.model).where(cls.model.id.in_(ids))
        result = await db.session.execute(statement)
        return result.scalars().all()
