from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class TTSRequestDTO(BaseModel):
    ref_text: str
    gen_text: str

    speed: float = Field(default=1.0, ge=0.5, le=2.0)
    remove_silence: bool = True
    match_duration: bool = True
    seed: Optional[int] = None


class TTSResponseDTO(BaseModel):
    audio: bytes

    # def save(self, path: Path):
    #     path.write_bytes(self.audio)
