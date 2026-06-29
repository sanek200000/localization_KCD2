from pathlib import Path

import requests

from app.config import SS
from app.exceptions.tts import TTSConnectionError, TTSServerError
from app.schemas.tts import TTSRequestDTO


class TTSClient:
    """
    Клиент для взаимодействия с TTS-сервером (Text-to-Speech).

    Реализует HTTP-интерфейс для отправки запроса на генерацию речи
    с использованием референсного аудио и текстовых параметров.
    Поддерживает контекстное управление ресурсами через Session.

    Attributes:
        _session (requests.Session): HTTP-сессия для повторного
            использования соединений.
        _server_url (str): Базовый URL TTS-сервера.
        _timeout (int | float): Таймаут запроса к серверу.
    """
    def __init__(self) -> None:
        self._session = requests.Session()
        self._server_url = SS.tts_server_url.rstrip("/")
        self._timeout = SS.tts_timeout

    def close(self):
        """
        Закрывает HTTP-сессию клиента.

        Returns:
            None

        Notes:
            Должен вызываться для освобождения сетевых ресурсов,
            если клиент используется вне контекстного менеджера.
        """
        self._session.close()

    def __enter__(self):
        """
        Вход в контекстный менеджер.

        Returns:
            TTSClient: текущий экземпляр клиента.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Выход из контекстного менеджера.

        Автоматически закрывает HTTP-сессию независимо от результата
        выполнения блока `with`.

        Args:
            exc_type: тип исключения (если произошло).
            exc_val: значение исключения.
            exc_tb: traceback исключения.

        Returns:
            None
        """
        self.close()

    def generate(self, ref_audio: Path, request: TTSRequestDTO) -> bytes:
        """
        Отправляет запрос на TTS-сервер для генерации аудио.

        Использует референсное аудио и параметры текста для генерации
        синтезированной речи.

        Args:
            ref_audio (Path): Путь к WAV-файлу референсного аудио.
            request (TTSRequestDTO): DTO с параметрами генерации речи
                (референсный текст, целевой текст и др.).

        Returns:
            bytes: Сгенерированный аудиофайл в бинарном формате.

        Raises:
            TTSConnectionError: Ошибка сетевого соединения или таймаута.
            TTSServerError: Некорректный ответ сервера (status != 200).

        Notes:
            - Отправляет multipart/form-data запрос на endpoint `/tts`.
            - Поля DTO сериализуются в строковый формат.
            - При ошибке сервера пытается извлечь JSON `detail`.
        """
        try:
            with ref_audio.open("rb") as file:
                files = {"ref_audio": (ref_audio.name, file, "audio/wav")}

                data = {
                    key: str(value)
                    for key, value in request.model_dump(exclude_none=True).items()
                }

                response = self._session.post(
                    url=f"{self._server_url}/tts",
                    files=files,
                    data=data,
                    timeout=self._timeout,
                )
        except requests.ConnectionError as ex:
            raise TTSConnectionError(str(ex)) from ex
        except requests.Timeout as ex:
            raise TTSConnectionError(str(ex)) from ex

        if response.status_code != 200:
            try:
                detail = response.json()
            except Exception:
                detail = response.text
            raise TTSServerError(f"{response.status_code}: {detail}")

        return response.content
