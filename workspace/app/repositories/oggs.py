from app.models.oggs import OggsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import OggsDataMapper


class OggsRepository(BaseRepository):
    """
    Репозиторий для работы с сущностью OGG-файлов.

    Предоставляет CRUD-операции и доступ к данным таблицы `oggs`
    через SQLAlchemy, а также преобразование ORM-объектов в DTO
    через `OggsDataMapper`.

    Attributes:
        model (Type[OggsOrm]): ORM-модель таблицы OGG-файлов.
        mapper (Type[OggsDataMapper]): Маппер для преобразования
            ORM-объектов в доменные DTO и обратно.
    """
    model = OggsOrm
    mapper = OggsDataMapper
