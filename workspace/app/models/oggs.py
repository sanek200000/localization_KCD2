from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class OggsOrm(Base):
    """
    ORM-модель таблицы с метаданными OGG-файлов.

    Таблица хранит информацию об аудиофайлах, включая уникальное имя,
    хеш содержимого и путь к файлу в файловой системе.

    Attributes:
        id (int): Первичный ключ записи.
        hash (str): Хеш аудиофайла для проверки уникальности
            или целостности данных.
        name (str): Уникальное имя аудиофайла без расширения.
        path (str): Полный путь к OGG-файлу в файловой системе.
    """

    __tablename__ = "en_oggs"

    id: Mapped[int] = mapped_column(primary_key=True)
    hash: Mapped[str] = mapped_column(String(15))
    name: Mapped[str] = mapped_column(String(50), unique=True)
    path: Mapped[str]
