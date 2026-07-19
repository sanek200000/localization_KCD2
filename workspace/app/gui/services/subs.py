from app.repositories.subs import SubsRepository


class SubsService:
    def __init__(self, session) -> None:
        self.repo = SubsRepository(session)

    async def get_page(self, offset: int, limit: int):
        return await self.repo.get_all(offset=offset, limit=limit)

    async def count(self):
        return await self.repo.count()


class GuiSubsService:
    def __init__(self, repository: SubsRepository) -> None:
        self.repository = repository

    def get_page(self, *, offset: int, limit: int, search: str = ""):
        return self.repository.get_page_with_oggs(
            offset=offset,
            limit=limit,
            search=search or None,
        )

    def count(self, search: str = ""):
        return self.repository.count(search or None)

    def get(self, sub_id: int):
        return self.repository.get_one(id=sub_id)
