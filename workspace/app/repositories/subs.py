from app.models.subs import SubsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import SubsDataMapper


class SubsRepository(BaseRepository):
    model = SubsOrm
    mapper = SubsDataMapper

    def get_null_accent(self):
        return self.get_filtred(
            self.model.ru_accent.is_(None), self.model.ru_sub.is_not(None)
        )
