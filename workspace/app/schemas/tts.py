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

    def format_log(self, ref_audio: str, target_audio: str) -> str:
        return (
            "\n"
            "========================================================\n"
            "Request\n"
            "--------------------------------------------------------\n"
            f"ref_text : {self.ref_text}\n"
            f"gen_text : {self.gen_text}\n"
            f"speed    : {self.speed:.2f}\n"
            f"seed     : {self.seed}\n"
            "\n"
            "Files\n"
            "--------------------------------------------------------\n"
            f"ref_audio : {ref_audio} \n"
            f"target_audio  : {target_audio} \n"
            "========================================================"
            "\n"
        )


class TTSResponseDTO(BaseModel):
    """
    Pydantic-модель для ответа TTS-сервиса.

    Содержит сгенерированный аудиофайл в бинарном формате.

    Attributes:
        audio (bytes): Сгенерированное аудио.
    """

    audio: bytes
