from collections.abc import Iterator
from typing import Type

from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

from app.db import Base
from app.repositories.mappers.base import DataMapper


class BaseRepository:
    """
    Базовый репозиторий для работы с ORM-моделями.

    Реализует стандартный набор CRUD-операций и предоставляет
    единый интерфейс доступа к данным через SQLAlchemy.

    Конкретные репозитории должны наследоваться от данного класса
    и определить атрибуты `model` и `mapper`.

    Attributes:
        model (Type[Base]): ORM-модель SQLAlchemy.
        mapper (Type[DataMapper]): Маппер для преобразования
            ORM-объектов в доменные сущности и обратно.
        session (Session): Активная сессия базы данных.
    """

    model: Type[Base] = None
    mapper: Type[DataMapper] = None

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_iter(self, batch_size: int, options=tuple()) -> Iterator:
        """
        Возвращает итератор по объектам репозитория с пакетной загрузкой.

        Выполняет потоковое чтение записей из базы данных, загружая их
        пакетами указанного размера (`yield_per`). Каждый ORM-объект
        автоматически преобразуется в соответствующую DTO с помощью
        зарегистрированного `DataMapper`.

        Такой подход позволяет обрабатывать большие объемы данных без
        загрузки всех записей в память одновременно.

        Args:
            batch_size (int): Количество объектов, загружаемых из базы
                данных за один пакет.
            options (tuple, optional): Опции SQLAlchemy для настройки
                загрузки связанных сущностей (например, `selectinload`,
                `joinedload`). По умолчанию пустой кортеж.

        Yields:
            BaseModel: Экземпляры доменной DTO, соответствующие
            записям ORM-модели.

        Notes:
            - Для потоковой загрузки используется параметр
            `execution_options(yield_per=batch_size)`.
            - Метод особенно эффективен при обработке большого числа
            записей, поскольку не материализует весь результат
            запроса в памяти.
        """

        stmt = (
            select(self.model).options(*options).execution_options(yield_per=batch_size)
        )
        result = self.session.scalars(stmt)

        for orm_obj in result:
            yield self.mapper.map_to_domain_entity(orm_obj)

    def get_filtred(self, *filter, options=tuple(), **filter_by):
        """
        Получает список записей с применением SQLAlchemy-фильтров и опций.

        Позволяет комбинировать позиционные выражения фильтрации
        (`filter`) с именованными условиями (`filter_by`), а также
        передавать дополнительные опции загрузки отношений через
        параметр `options`.

        Args:
            *filter: SQLAlchemy-выражения фильтрации, например
                `Model.field == value`.
            options (tuple, optional): Опции SQLAlchemy для настройки
                загрузки связанных сущностей (`joinedload`,
                `selectinload` и др.). По умолчанию пустой кортеж.
            **filter_by: Именованные параметры фильтрации,
                соответствующие полям ORM-модели.

        Returns:
            list: Список объектов ORM-модели, удовлетворяющих условиям
            запроса.
        """
        query = (
            select(self.model).options(*options).filter(*filter).filter_by(**filter_by)
        )
        result = self.session.execute(query)
        return result.scalars().all()

    def get_all(self, *args, **kwargs):
        """
        Получает все записи модели.

        Является сокращением для вызова метода `get_filtred()`
        без условий фильтрации.

        Args:
            *args: Зарезервировано для совместимости интерфейса.
            **kwargs: Зарезервировано для совместимости интерфейса.

        Returns:
            list: Список всех объектов ORM-модели.
        """
        return self.get_filtred()

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

    def get_one(self, **filter_by):
        """
        Получает одну запись по заданным критериям фильтрации.

        Args:
            **filter_by: Именованные параметры фильтрации,
                соответствующие полям ORM-модели.

        Returns:
            Base: Найденный ORM-объект.

        Raises:
            sqlalchemy.exc.NoResultFound:
                Если запись не найдена.
            sqlalchemy.exc.MultipleResultsFound:
                Если найдено более одной записи.
        """
        query = select(self.model).filter_by(**filter_by)
        result = self.session.execute(query)
        return result.scalars().one()

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

    def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        """
        Обновляет записи, удовлетворяющие условиям фильтрации.

        Значения для обновления извлекаются из переданной
        Pydantic-модели.

        Args:
            data (BaseModel): Модель с новыми данными.
            exclude_unset (bool, optional): Если `True`, в запрос
                включаются только явно заданные поля модели.
                По умолчанию `False`.
            **filter_by: Условия фильтрации записей для обновления.

        Returns:
            None
        """
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        self.session.execute(stmt)

    def delete(self, **kwargs):
        """
        Удаляет записи, удовлетворяющие условиям фильтрации.

        Args:
            **kwargs: Именованные параметры фильтрации,
                соответствующие полям ORM-модели.

        Returns:
            None
        """
        query = delete(self.model).filter_by(**kwargs)
        self.session.execute(query)
