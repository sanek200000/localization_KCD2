from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


if TYPE_CHECKING:
    from app.models.subs import SubsOrm


class OggsOrm(Base):
    """
    ORM-модель таблицы аудиофайлов.

    Хранит информацию о путях к английским и русским аудиофайлам,
    а также связь с соответствующей записью субтитров.

    Attributes:
        id (int): Первичный ключ записи.
        key (str): Внешний ключ, ссылающийся на поле `key`
            таблицы `subs`.
        name (str): Уникальное имя аудиофайла.
        ogg_en_path (str): Путь к английскому OGG-файлу.
        wav_en_path (str): Путь к английскому WAV-файлу.
        ogg_ru_path (str): Путь к русскому OGG-файлу.
        wav_ru_path (str): Путь к русскому WAV-файлу.
        sub (SubsOrm): Связанный объект субтитров.
    """

    __tablename__ = "oggs"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(ForeignKey("subs.key"), index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    ogg_en_path: Mapped[str]
    wav_en_path: Mapped[str]
    ogg_ru_path: Mapped[str]
    wav_ru_path: Mapped[str]

    sub: Mapped["SubsOrm"] = relationship(back_populates="oggs")
