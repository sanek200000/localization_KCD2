from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class TTSRequestDTO(BaseModel):
    """
    Pydantic-модель для запроса на генерацию речи через TTS-сервис.

    Описывает параметры синтеза речи, включая референсный текст,
    целевой текст и параметры генерации аудио.

    Attributes:
        ref_text (str): Референсный текст, соответствующий
            входному аудио (speaker conditioning).
        gen_text (str): Текст, который необходимо синтезировать
            в аудио.
        speed (float): Скорость речи. Ограничена диапазоном
            от 0.5 до 2.0. Значение по умолчанию — 1.0.
        remove_silence (bool): Удаление пауз/тишины в аудио.
        match_duration (bool): Подгон длительности аудио под
            референс.
        seed (Optional[int]): Seed для воспроизводимости генерации.
    """
    ref_text: str
    gen_text: str

    speed: float = Field(default=1.0, ge=0.5, le=2.0)
    remove_silence: bool = True
    match_duration: bool = True
    seed: Optional[int] = None


class TTSResponseDTO(BaseModel):
    """
    Pydantic-модель для ответа TTS-сервиса.

    Содержит сгенерированный аудиофайл в бинарном формате.

    Attributes:
        audio (bytes): Сгенерированное аудио.
    """
    audio: bytes

