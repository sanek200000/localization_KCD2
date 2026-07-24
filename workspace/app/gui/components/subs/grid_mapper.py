from pathlib import Path

from app.schemas.subs import SubDTO


def to_grid_row(sub: SubDTO) -> dict:
    is_audio = all(Path(ogg.wav_ru_path).exists() for ogg in sub.oggs)
    return {
        "id": sub.id,
        "key": sub.key,
        "en_sub": sub.en_sub,
        "ru_sub": sub.ru_sub,
        "accent": sub.ru_accent,
        "ru_audio": "✅" if is_audio else "❌",
        "audio_count": len(sub.oggs) if sub.oggs else 0,
    }
