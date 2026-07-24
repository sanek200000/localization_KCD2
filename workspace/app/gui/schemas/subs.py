from loguru import logger
from pydantic import BaseModel, ConfigDict, Field

from app.api.subs import get_id_position
from app.gui.services.subs import GuiSubsService
from app.schemas.subs import SubDTO


class SubtitlesStateDTO(BaseModel):
    """
    DTO, хранящий состояние списка субтитров для отображения с поддержкой
    пагинации и поиска.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    page: int = 0
    page_size: int = 100
    search: str = ""
    total: int = 0

    rows: list[SubDTO] = Field(default_factory=list)

    @property
    def offset(self) -> int:
        """
        Возвращает смещение первой записи текущей страницы.

        Returns:
            Смещение относительно начала полного списка.
        """
        return self.page * self.page_size

    @property
    def ids(self) -> list[int]:
        """
        Возвращает идентификаторы всех субтитров, загруженных на текущей странице.

        Returns:
            Список идентификаторов субтитров.
        """
        # logger.debug(f"{len(self.rows) = }")
        return [row.id for row in self.rows]

    @property
    def pages(self) -> int:
        """
        Возвращает общее количество доступных страниц.

        Returns:
            Количество страниц с учетом общего числа записей и размера страницы.
        """
        if self.total == 0:
            return 1
        return (self.total - 1) // self.page_size + 1

    def reload(self) -> None:
        """
        Обновляет состояние списка субтитров.

        Выполняет пересчет общего количества записей и загружает данные
        для текущей страницы с учетом поискового запроса.
        """
        self.total = GuiSubsService.count(search=self.search)

        self.rows = GuiSubsService.get_page(
            offset=self.offset,
            limit=self.page_size,
            search=self.search,
        )

    def clear(self) -> None:
        """
        Сбрасывает состояние списка субтитров.

        Возвращает номер страницы и поисковый запрос к значениям по умолчанию
        и очищает текущий список записей.
        """
        self.page = 0
        self.search = ""
        self.rows.clear()

    def restore(self, id: int):
        self.clear()
        pos = get_id_position(id=id)
        offset = max(0, pos - self.page_size // 2)
        # logger.info(f"{id = }\t{pos = }\t{offset = }")

        self.rows = GuiSubsService.get_page(
            offset=offset,
            limit=self.page_size,
            search=self.search,
        )
