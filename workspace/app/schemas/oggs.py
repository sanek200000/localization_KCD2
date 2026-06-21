from pydantic import BaseModel


class OggAdd(BaseModel):
    """
    Pydantic-модель для создания записи об аудиофайле.

    Содержит идентификатор субтитра и пути к связанным аудиофайлам
    на английском и русском языках в форматах OGG и WAV.

    Attributes:
        key (str): Уникальный идентификатор субтитра, с которым
            связан аудиофайл.
        name (str): Уникальное имя аудиофайла.
        ogg_en_path (str): Путь к английскому OGG-файлу.
        wav_en_path (str): Путь к английскому WAV-файлу.
        ogg_ru_path (str): Путь к русскому OGG-файлу.
        wav_ru_path (str): Путь к русскому WAV-файлу.
    """

    key: str
    name: str
    ogg_en_path: str
    wav_en_path: str
    ogg_ru_path: str
    wav_ru_path: str


class Ogg(OggAdd):
    """
    Модель данных (схема) для чтения идентификатора записи и хеша OGG-файла.

    Используется при получении информации из базы данных или другого
    хранилища, когда требуется сопоставление записи с её хешем.

    Attributes:
        id (int): Уникальный идентификатор записи.
    """

    id: int
