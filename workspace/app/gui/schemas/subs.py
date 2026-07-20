from pydantic import BaseModel


class SubtitlesStateDTO(BaseModel):
    page: int = 0
    page_size: int = 100

    total: int = 0

    search: str = ""
