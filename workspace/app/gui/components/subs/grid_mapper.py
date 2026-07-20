from app.schemas.subs import SubDTO


def to_grid_row(sub: SubDTO) -> dict:
    return {
        "id": sub.id,
        "key": sub.key,
        "en_sub": sub.en_sub,
        "ru_sub": sub.ru_sub,
        "accent": sub.ru_accent,
        "audio_count": len(sub.oggs) if sub.oggs else 0,
    }
