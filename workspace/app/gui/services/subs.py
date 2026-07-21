from app.api.subs import get_all_with_limit, get_db_count, get_sub
from app.schemas.subs import SubDTO


# class SubsService:
#     def __init__(self, session) -> None:
#         self.repo = SubsRepository(session)
#
#     async def get_page(self, offset: int, limit: int):
#         return await self.repo.get_all(offset=offset, limit=limit)
#
#     async def count(self):
#         return await self.repo.count()


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
        return get_db_count(search or None)

    @staticmethod
    def get(sub_id: int) -> SubDTO:
        return get_sub(id=sub_id)
