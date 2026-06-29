from pathlib import Path

import requests

from app.config import SS
from app.exceptions.tts import TTSConnectionError, TTSServerError
from app.schemas.tts import TTSRequestDTO


class TTSClient:
    def __init__(self) -> None:
        self._session = requests.Session()
        self._server_url = SS.tts_server_url.rstrip("/")
        self._timeout = SS.tts_timeout

    def close(self):
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def generate(self, ref_audio: Path, request: TTSRequestDTO) -> bytes:
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
