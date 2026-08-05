import requests
from pathlib import Path
from time import sleep
from time import perf_counter as pc

from loguru import logger
from requests.exceptions import HTTPError

from app.config import RS, SS
from app.exceptions.tts import TTSConnectionError, TTSServerError
from app.schemas.jobs import JobStatus, JobCreateResponseDTO, JobStatusResponseDTO
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
        self._server_url = RS.tts_server_url.rstrip("/")
        self._timeout = SS.tts_timeout
        # logger.info(f"TTSClient created: {id(self)}")

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

    def ping(self) -> dict:
        try:
            response = self._session.get(
                f"{self._server_url}/f5tts",
                timeout=30,
            )
            return response.json()
        except (
            requests.ConnectionError,
            requests.Timeout,
            HTTPError,
        ):
            return {"status": "no connection"}

    def check_model(self) -> str | dict:
        try:
            response = self._session.get(
                f"{self._server_url}/f5tts/model/current",
                timeout=30,
            )
            rsp = response.json()
            name = rsp.get("model").get("name")
            path = rsp.get("model").get("ckpt_path")

            return " ".join((name, path))
        except (
            requests.ConnectionError,
            requests.Timeout,
            HTTPError,
            AttributeError,
        ):
            return {"status": "no model"}

    def get_models(self):
        try:
            response = self._session.get(
                f"{self._server_url}/f5tts/models",
                timeout=30,
            )
            return response.json()
        except requests.ConnectionError:
            models = "No connect to TTS server"
            logger.error(models)
            raise
        except requests.Timeout:
            models = "Превышено время ожидания ответа от TTS-сервера."
            logger.error(models)
            raise
        except HTTPError as he:
            models = f"Сервер ответил с ошибкой"
            logger.error(f"Сервер ответил с ошибкой: {he.response.status_code}")
            raise
        except Exception as ex:
            logger.error(f"{type(ex)} {ex}")
            raise

    def change_model(self, model_id: int):
        try:
            response = self._session.post(
                f"{self._server_url}/f5tts/model/load/{model_id}",
                timeout=30,
            )
            logger.info(response.json())
        except Exception as ex:
            logger.error(f"{type(ex)} {ex}")
            raise

        return response.json()

    def generate(self, ref_audio: Path, request: TTSRequestDTO) -> bytes:
        total = pc()  # TODO: delete
        logger.info("generate() entered")  # TODO: delete

        poll_interval = 1
        max_connection_errors = 10
        connection_errors = 0

        t = pc()  # TODO: delete
        logger.info("POST /tts started")  # TODO: delete

        job_id = self._create_job(ref_audio, request)
        logger.info(f"Created TTS job: {job_id}")

        logger.info(f"Post /tts {pc() - t} sec")  # TODO: delete

        poll_start = pc()  # TODO: delete
        while True:
            try:
                status = self._get_job_status(job_id)
                connection_errors = 0
            except TTSConnectionError:
                connection_errors += 1
                logger.warning(
                    f"Unable to get status for job '{job_id}' "
                    f"({connection_errors}/{max_connection_errors})"
                )

                if connection_errors >= max_connection_errors:
                    logger.error(
                        f"connection_errors >= max_connection_errors ({connection_errors = })"
                    )
                    raise

                sleep(poll_interval)
                continue
            except Exception as ex:
                connection_errors += 1
                if connection_errors >= max_connection_errors:
                    logger.error(
                        f"connection_errors >= max_connection_errors ({connection_errors = })"
                    )
                    raise

                logger.error(f"{type(ex)} {ex}")

            logger.debug(
                f"Job '{job_id}': "
                f"{status.status}, "
                f"attempt={status.current_attempt}/{status.max_attempts}, "
                f"similarity={status.similarity}"
            )

            if status.status is JobStatus.COMPLETED:
                t = pc()  # TODO: delete

                result = self._download_reault(job_id)

                logger.info(f"Download {pc() - t} sec")  # TODO: delete
                logger.info(f"Polling {pc() - poll_start} sec")  # TODO: delete
                logger.info(f"TOTAL generate {pc() - total} sec")  # TODO: delete

                return result

            if status.status is JobStatus.FAILED:
                detail = status.error or "TTS generation failed"
                logger.error(detail)

                logger.info(f"Polling {pc() - poll_start} sec")  # TODO: delete
                logger.info(f"TOTAL generate {pc() - total} sec")  # TODO: delete

                raise TTSServerError(detail)

            sleep(poll_interval)

        logger.info(f"Polling {pc() - poll_start} sec")  # TODO: delete

    def _create_job(self, ref_audio: Path, request: TTSRequestDTO) -> str:
        try:
            with ref_audio.open("rb") as file:
                files = {"ref_audio": (ref_audio.name, file, "audio/wav")}

                data = {
                    key: str(value)
                    for key, value in request.model_dump(exclude_none=True).items()
                }

                response = self._session.post(
                    url=f"{self._server_url}/f5tts/tts",
                    files=files,
                    data=data,
                    timeout=self._timeout,
                )
        except requests.ConnectionError as ex:
            logger.error(TTSConnectionError(str(ex)))
            raise TTSConnectionError(str(ex)) from ex
        except requests.Timeout as ex:
            logger.error(TTSConnectionError(str(ex)))
            raise TTSConnectionError(str(ex)) from ex

        if response.status_code != 200:
            try:
                detail = response.json()
            except Exception:
                detail = response.text
            logger.error(TTSServerError(f"{response.status_code}: {detail}"))
            raise TTSServerError(f"{response.status_code}: {detail}")

        job = JobCreateResponseDTO.model_validate(response.json())

        return job.id

    def _get_job_status(self, job_id: str) -> JobStatusResponseDTO:
        try:
            response = self._session.get(
                f"{self._server_url}/f5tts/job/{job_id}",
                timeout=30,
            )
            return JobStatusResponseDTO.model_validate(response.json())
        except Exception as ex:
            logger.error(f"{type(ex)} {ex}")
            raise

    def _download_reault(self, job_id: str) -> bytes:
        try:
            response = self._session.get(
                f"{self._server_url}/f5tts/job/{job_id}/result",
                timeout=30,
            )

            result = response.content
            if isinstance(result, bytes):
                return result

            logger.warning(f"Failed generation: {result}")
        except Exception as ex:
            logger.error(f"{type(ex)} {ex}")

    @property
    def server_url(self):
        return self._server_url
