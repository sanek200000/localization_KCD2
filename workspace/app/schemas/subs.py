from typing import Optional

from pydantic import BaseModel

from app.schemas.oggs import OggDTO


class SubAddDTO(BaseModel):
    """
    Pydantic-модель для создания записи субтитра.

    Содержит исходный текст, перевод и версию текста с ударениями,
    используемую для синтеза речи.

    Attributes:
        key (str): Уникальный идентификатор субтитра.
        en_sub (str): Исходный текст на английском языке.
        ru_sub (str): Перевод текста на русский язык.
        ru_accent (str): Русский текст с расставленными ударениями.
    """

    key: str
    en_sub: Optional[str] = None
    ru_sub: str
    ru_accent: Optional[str] = None


class SubDTO(SubAddDTO):
    """
    Pydantic-модель субтитра, содержащая идентификатор записи.

    Расширяет модель `SubsAdd`, добавляя первичный ключ базы данных.

    Attributes:
        id (int): Уникальный идентификатор записи в базе данных.
    """

    id: int
    oggs: Optional[list[OggDTO]] = None
