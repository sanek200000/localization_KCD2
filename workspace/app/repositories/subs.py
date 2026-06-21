from app.models.subs import SubsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import SubsDataMapper


class SubsRepository(BaseRepository):
    model = SubsOrm
    mapper = SubsDataMapper
