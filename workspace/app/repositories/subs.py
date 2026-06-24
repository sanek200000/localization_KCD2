from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.subs import SubsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import SubsDataMapper


class SubsRepository(BaseRepository):
    """
    Репозиторий для работы с сущностью субтитров.

    Предоставляет методы получения и изменения записей таблицы
    `subs`, а также специализированные выборки, связанные
    с обработкой и озвучиванием субтитров.

    Attributes:
        model (Type[SubsOrm]): ORM-модель субтитров.
        mapper (Type[SubsDataMapper]): Маппер для преобразования
            ORM-объектов в доменные сущности.
    """
    model = SubsOrm
    mapper = SubsDataMapper

    def get_null_accent(self):
        """
        Получает субтитры, для которых еще не расставлены ударения.

        Возвращает записи, у которых поле `ru_accent` имеет значение
        `NULL`, но при этом присутствует перевод в поле `ru_sub`.

        Используется для поиска субтитров, ожидающих обработки
        модулем расстановки ударений.

        Returns:
            list[Subs]: Список субтитров без заполненного поля
            `ru_accent`.

        Notes:
            При необходимости можно дополнительно загружать связанные
            аудиофайлы через `selectinload(self.model.oggs)`.
        """
        return self.get_filtred(
            self.model.ru_accent.is_(None),
            self.model.ru_sub.is_not(None),
            # options=(selectinload(self.model.oggs),),
        )
