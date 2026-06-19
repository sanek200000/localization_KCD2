from typing import Type

from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import Base
from app.repositories.mappers.base import DataMapper


class BaseRepository:
    """
    Базовый репозиторий для выполнения типовых операций с ORM-моделями.

    Предоставляет общий интерфейс для работы с таблицами базы данных
    через SQLAlchemy. Конкретные репозитории должны наследоваться от
    данного класса и определять атрибут `model`, содержащий ORM-модель.

    Attributes:
        model (Type[Base]): ORM-модель SQLAlchemy, с которой работает
            репозиторий.
        session (Session): Активная сессия базы данных.
    """

    model: Type[Base] = None
    # schema: Type[BaseModel] = None
    mapper: Type[DataMapper] = None

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self, *args, **kwargs):
        """
        Получает все записи из таблицы, связанной с моделью репозитория.

        Args:
            *args: Зарезервировано для будущих расширений.
            **kwargs: Зарезервировано для будущих расширений.

        Returns:
            list[Base]: Список объектов ORM-модели.
        """
        query = select(self.model)
        result = self.session.execute(query)
        return result.scalars().all()

    def get_one_or_none(self, **filter_by):
        """
        Получает одну запись по заданным критериям фильтрации.

        Формирует запрос к таблице, связанной с моделью репозитория,
        используя параметры из `filter_by`. Если запись найдена,
        возвращается соответствующий ORM-объект. Если запись отсутствует,
        возвращается `None`.

        Args:
            **filter_by: Именованные параметры фильтрации, соответствующие
                полям ORM-модели.

        Returns:
            Base | None: Найденный ORM-объект или `None`, если запись
            не существует.
        """
        query = select(self.model).filter_by(**filter_by)
        result = self.session.execute(query)
        return result.scalars().one_or_none()

    def add(self, data: BaseModel):
        """
        Создает новую запись в базе данных.

        Данные извлекаются из Pydantic-модели и вставляются в таблицу,
        связанную с текущей ORM-моделью. После вставки возвращается
        созданный объект.

        Args:
            data (BaseModel): Pydantic-модель с данными для создания записи.

        Returns:
            Base: Созданный ORM-объект.
        """
        "sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: en_oggs.name"
        stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .prefix_with("OR IGNORE")
            .returning(self.model)
        )
        result = self.session.execute(stmt)
        res = result.scalars().one_or_none()
        if res:
            return self.mapper.map_to_domain_entity(res)
