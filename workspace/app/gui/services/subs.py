from app.repositories.subs import SubsRepository


class SubsService:
    def __init__(self, session) -> None:
        self.repo = SubsRepository(session)

    async def get_page(self, offset: int, limit: int):
        return await self.repo.get_all(offset=offset, limit=limit)

    async def count(self):
        return await self.repo.count()
