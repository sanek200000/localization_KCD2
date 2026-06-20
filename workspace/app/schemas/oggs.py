from pydantic import BaseModel, ConfigDict


class OggAdd(BaseModel):
    """
    Модель данных (схема) для добавления информации об OGG-файле.

    Используется при добавлении новых записей в хранилище, а также
    для преобразования ORM-объектов в Pydantic-модели благодаря
    настройке `from_attributes=True`.

    Attributes:
        hash (str): Уникальный хеш аудиофайла.
        name (str): Имя файла или идентификатор аудио.
        path (str): Полный путь к OGG-файлу в файловой системе.
    """

    hash: str
    name: str
    ogg_en_path: str
    wav_en_path: str
    ogg_ru_path: str
    wav_ru_path: str


class Oggs(OggAdd):
    """
    Модель данных (схема) для чтения идентификатора записи и хеша OGG-файла.

    Используется при получении информации из базы данных или другого
    хранилища, когда требуется сопоставление записи с её хешем.

    Attributes:
        id (int): Уникальный идентификатор записи.
    """

    id: int
