from app.repositories.mappers.base import DataMapper
from app.models.oggs import OggsOrm
from app.models.subs import SubsOrm
from app.schemas.oggs import Ogg
from app.schemas.subs import Sub


class OggsDataMapper(DataMapper):
    """
    Маппер для преобразования данных OGG-файлов между ORM-моделью
    и Pydantic-схемой.

    Наследует базовую функциональность от `DataMapper` и определяет
    соответствие между моделью хранения данных `OggsOrm` и доменной
    схемой `Oggs`.

    Attributes:
        model (Type[OggsOrm]): ORM-модель таблицы OGG-файлов.
        schema (Type[Oggs]): Pydantic-схема представления OGG-файла.

    Examples:
        Преобразование ORM-объекта в схему:

        >>> schema_obj = OggsDataMapper.map_to_domain_entity(orm_obj)

        Преобразование схемы в ORM-объект:

        >>> orm_obj = OggsDataMapper.map_to_persistence_entity(schema_obj)
    """

    model = OggsOrm
    schema = Ogg


class SubsDataMapper(DataMapper):
    model = SubsOrm
    schema = Sub
