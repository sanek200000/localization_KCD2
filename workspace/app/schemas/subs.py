from typing import Optional

from pydantic import BaseModel

from app.schemas.oggs import Ogg


class SubAdd(BaseModel):
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
    en_sub: str
    ru_sub: str
    ru_accent: str


class Sub(SubAdd):
    """
    Pydantic-модель субтитра, содержащая идентификатор записи.

    Расширяет модель `SubsAdd`, добавляя первичный ключ базы данных.

    Attributes:
        id (int): Уникальный идентификатор записи в базе данных.
    """

    id: int
    oggs: Optional[list[Ogg]] = None
