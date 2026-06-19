from typing import Type

from pydantic import BaseModel

from app.db import Base


class DataMapper:
    """
    Базовый класс для преобразования данных между слоями приложения.

    Реализует паттерн Data Mapper, обеспечивая конвертацию между
    ORM-моделями (слой хранения данных) и Pydantic-схемами
    (доменный слой или слой передачи данных).

    Атрибуты `model` и `schema` должны быть переопределены
    в классах-наследниках.

    Attributes:
        model (Type[Base]): ORM-модель SQLAlchemy.
        schema (Type[BaseModel]): Pydantic-схема, соответствующая модели.
    """

    model: Type[Base] = None
    schema: Type[BaseModel] = None

    @classmethod
    def map_to_domain_entity(cls, data: Type[Base]):
        """
        Преобразует ORM-объект в экземпляр Pydantic-схемы.

        Args:
            data (Base): ORM-объект SQLAlchemy.

        Returns:
            BaseModel: Экземпляр схемы, указанной в атрибуте `schema`.

        Notes:
            Использует `model_validate(..., from_attributes=True)`,
            что позволяет извлекать данные напрямую из атрибутов
            ORM-объекта.
        """
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data: Type[BaseModel]):
        """
        Преобразует Pydantic-схему в ORM-объект.

        Args:
            data (BaseModel): Экземпляр Pydantic-схемы.

        Returns:
            Base: Экземпляр ORM-модели, указанной в атрибуте `model`.

        Notes:
            Для формирования ORM-объекта используется результат
            метода `model_dump()`.
        """
        return cls.model(**data.model_dump())
