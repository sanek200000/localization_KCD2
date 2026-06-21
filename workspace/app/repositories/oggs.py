from app.models.oggs import OggsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import OggsDataMapper


class OggsRepository(BaseRepository):
    model = OggsOrm
    mapper = OggsDataMapper
