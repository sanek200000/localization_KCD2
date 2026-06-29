#!/usr/bin/env python3

from pathlib import Path
from helper import load_marshal, append_txt

DB = Path("./temp/db_with_pathes_and_accent.bin")
SAFETENSORS_MISHA = "./models/F5-TTS_RUSSIAN_misha/F5TTS_v1_Base_accent_tune/model_last_inference.safetensors"
VOCAB_MISHA = "./models/F5-TTS_RUSSIAN_misha/F5TTS_v1_Base/vocab.txt"

KEYS_WITHOUT_RUSUB = Path('./temp/keys_without_rusub.txt').resolve()


def change_speed(text: str):
    len_text = len(text.split(" "))
    print(f"{len_text = }")

    if len_text in range(3, 10):
        return 0.7
    elif len_text > 10:
        return 0.9
    elif len_text == 1:
        return 0.3
    return 0.5


def convert_audio_en_to_ru(data: dict):
    """
    Генерирует русскоязычные аудиофайлы с использованием модели F5-TTS.

    Для каждого элемента словаря `data` функция берет эталонное аудио
    (`wav_en_path`) и соответствующий английский текст (`en_sub`),
    после чего выполняет синтез речи на русском языке и сохраняет
    результат в файл, указанный в `wav_ru_path`.

    Если целевой аудиофайл уже существует, генерация для данного
    элемента пропускается.

    Args:
        data (dict): Словарь вида:
            {
                "<key>": {
                    "wav_en_path": "<путь к эталонному аудио>",
                    "en_sub": "<английский текст>",
                    "ru_sub": "<русский текст>",
                    "wav_ru_path": "<путь для сохранения результата>",
                    ...
                },
                ...
            }

    Returns:
        None

    Side Effects:
        - Загружает модель F5-TTS.
        - Создает отсутствующие директории для выходных файлов.
        - Генерирует и сохраняет WAV-файлы с частотой дискретизации 24000 Гц.
        - Записывает аудиоданные на диск.

    Notes:
        - В текущей реализации для синтеза используется тестовая строка,
          переданная в параметр `gen_text`, а не значение поля `ru_sub`.
        - При включенном режиме DEBUG обрабатывается только первый
          подходящий элемент словаря.
        - Ключ `"nothing"` пропускается.
    """
    from f5_tts.api import F5TTS
    import soundfile as sf

    DEBUG = 0
    tts = F5TTS(
        ckpt_file=SAFETENSORS_MISHA,
        vocab_file=VOCAB_MISHA,
        device="cpu",
    )

    len_data = len(data)
    for i, (key, value) in enumerate(data.items(), start=1):
        if DEBUG and i == 30:
            break
        if key == "nothing":
            continue

        ref_audio = value.get("wav_en_path")
        ref_text = value.get("en_sub")  # важно для качества
        target_audio = Path(value.get("wav_ru_path"))
        target_text = value.get("ru_sub_accent")

        if target_audio.exists():
            continue

        print(f"\n\n{i}/{len_data}")
        if not target_text:
            print('No ru_sub_accent')
            append_txt(KEYS_WITHOUT_RUSUB, key)
            continue

        # speed = change_speed(target_text)
        target_audio.parent.mkdir(parents=True, exist_ok=True)

        wav, sr, spec = tts.infer(
            # speed=speed,
            ref_file=ref_audio,
            ref_text=ref_text,
            gen_text=target_text,
        )
        sf.write(target_audio, wav, 24000)


if __name__ == "__main__":
    pass

    data = load_marshal(DB)
    # print(len(data))
    convert_audio_en_to_ru(data)
