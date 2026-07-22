from pydantic import BaseModel, ConfigDict, Field

from app.gui.services.subs import GuiSubsService
from app.schemas.subs import SubDTO


class SubtitlesStateDTO(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    page: int = 0
    page_size: int = 100
    search: str = ""
    total: int = 0

    rows: list[SubDTO] = Field(default_factory=list)

    @property
    def offset(self) -> int:
        return self.page * self.page_size

    @property
    def ids(self) -> list[int]:
        return [row.id for row in self.rows]

    # @property
    # def total(self) -> int:
    #     return GuiSubsService.count(search=self.search)

    @property
    def pages(self) -> int:
        if self.total == 0:
            return 1
        return (self.total - 1) // self.page_size + 1

    def reload(self) -> None:
        self.total = GuiSubsService.count(search=self.search)

        self.rows = GuiSubsService.get_page(
            offset=self.offset,
            limit=self.page_size,
            search=self.search,
        )

    def clear(self) -> None:
        self.page = 0
        self.search = ""
        self.rows.clear()


