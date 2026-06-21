from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.oggs import OggsOrm


class SubsOrm(Base):
    """
    ORM-модель таблицы субтитров.

    Содержит оригинальный текст субтитра на английском языке,
    перевод на русский язык, версию текста с ударениями для
    синтеза речи, а также связь с соответствующими аудиофайлами.

    Attributes:
        id (int): Первичный ключ записи.
        key (str): Уникальный идентификатор субтитра, используемый
            для связи с аудиофайлами.
        en_sub (str): Исходный текст субтитра на английском языке.
        ru_sub (str): Перевод субтитра на русский язык.
        ru_accent (str): Русский текст с расставленными ударениями.
        oggs (list[OggsOrm]): Список связанных аудиофайлов,
            содержащих озвучку данного субтитра.
    """

    __tablename__ = "subs"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(15), unique=True, index=True)
    en_sub: Mapped[str]
    ru_sub: Mapped[str]
    ru_accent: Mapped[str]

    oggs: Mapped[list["OggsOrm"]] = relationship(back_populates="sub")
