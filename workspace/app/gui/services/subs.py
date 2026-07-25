from app.api.subs import get_all_with_limit, get_subs_count, get_sub
from app.schemas.subs import SubDTO


class GuiSubsService:
    @staticmethod
    def get_page(*, offset: int, limit: int, search: str = ""):
        return get_all_with_limit(
            offset=offset,
            limit=limit,
            search=search or None,
        )

    @staticmethod
    def count(search: str = ""):
        return get_subs_count(search or None)

    @staticmethod
    def get(sub_id: int) -> SubDTO:
        return get_sub(sub_id=sub_id)
