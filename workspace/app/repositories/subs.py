from collections.abc import Iterator

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
        )

    def get_subs_with_oggs(self):
        """
        Получает все субтитры с предзагруженными связанными OGG-записями.

        Выполняет запрос к таблице `subs` с использованием eager loading
        для связи `oggs`, чтобы избежать N+1 проблемы при доступе
        к связанным аудиофайлам.

        Returns:
            list[Subs]: Список субтитров с загруженными отношениями
            `oggs`.

        Notes:
            Используется `selectinload`, что оптимально для загрузки
            one-to-many связей.
        """
        return self.get_filtred(
            options=(selectinload(self.model.oggs),),
        )

    def iter_subs_with_oggs(self, batch_size: int) -> Iterator:
        """
        Итеративно получает субтитры с предзагруженными OGG-записями
        с использованием пакетной загрузки.

        Объединяет:
        - eager loading связи `oggs`
        - потоковую обработку через `yield_per`

        Позволяет обрабатывать большие наборы субтитров без загрузки
        всей выборки в память.

        Args:
            batch_size (int): Размер пакета для построчной выборки.

        Yields:
            Subs: DTO-объекты субтитров с загруженными OGG-связями.

        Notes:
            Подходит для ETL-задач и фоновой обработки аудиоданных.
        """
        return self.get_iter(
            options=(selectinload(self.model.oggs),),
            batch_size=batch_size,
        )
