from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel


class JobStatus(StrEnum):
    QUEUED = "queued"
    PROGRESSING = "progressing"
    COMPLETED = "comleted"
    FAILED = "failed"


class JobCreateResponseDTO(BaseModel):
    id: str


class JobStatusResponseDTO(JobCreateResponseDTO):
    status: JobStatus

    current_attempt: int
    max_attempts: int

    similarity: Optional[float] = None
    speed: Optional[float] = None

    created_at: datetime
    updated_at: datetime

    error: Optional[str] = None
