from pathlib import Path
from typing import Optional
from time import perf_counter as pc

from app.schemas.subs import SubDTO
from loguru import logger

from app.api.dependencies import inject_tts
from app.api.subs import get_all_subs_iter
from app.clients.tts import TTSClient
from app.schemas.tts import TTSRequestDTO

DB = Path("./temp/db_with_pathes_and_accent.bin")
SAFETENSORS_MISHA = "./models/F5-TTS_RUSSIAN_misha/F5TTS_v1_Base_accent_tune/model_last_inference.safetensors"
VOCAB_MISHA = "./models/F5-TTS_RUSSIAN_misha/F5TTS_v1_Base/vocab.txt"

KEYS_WITHOUT_RUSUB = Path("./temp/keys_without_rusub.txt").resolve()


@inject_tts
def get_server_url(tts_client: TTSClient) -> dict:
    return tts_client.server_url


@inject_tts
def check_tts_server_connection(tts_client: TTSClient) -> dict:
    return tts_client.ping()


@inject_tts
def check_tts_loaded_model(tts_client: TTSClient) -> str | dict:
    return tts_client.check_model()


@inject_tts
def get_models(tts_client: TTSClient) -> dict | str:
    try:
        models = tts_client.get_models()
    except Exception as ex:
        models = "No connect to TTS server"
        logger.error(f"Непредвиденная ошибка: {ex}")
    finally:
        return models


# @inject_tts
# def change_tts_server(tts_client: TTSClient, url: str) -> dict:
#     tts_client.reconnect(url)
#     logger.info(f"URL cnanging on {url}")


@inject_tts
def load_model(tts_client: TTSClient, id: int):
    return tts_client.change_model(model_id=id)


@inject_tts
def convert_audio_with_remote_session(
    tts_client: TTSClient,
    sub_id: int,
    ref_text: str,
    target_text: str,
    ref_audio: Path,
    target_audio: Path,
    change_dir: Optional[str] = None,
):
    total = pc()  # TODO: delete
    logger.info("Remote conversion started")  # TODO: delete

    if change_dir:
        new_parts = [
            f"ru_voice_wav_{change_dir}" if part == "ru_voice_wav" else part
            for part in target_audio.parts
        ]
        target_audio = Path(*new_parts)

    if target_audio.exists():
        logger.warning(f"file {str(target_audio)} is exists")
        return
    if not target_text:
        logger.warning(f"target_text in id={sub_id} is None")
        return

    target_audio.parent.mkdir(parents=True, exist_ok=True)

    request = TTSRequestDTO(
        ref_text=ref_text,
        gen_text=target_text,
    )
    try:
        generate_start = pc()  # TODO: delete
        logger.info("tts_client.generate() started")  # TODO: delete

        audio_bytes = tts_client.generate(ref_audio=ref_audio, request=request)

        logger.info(
            f"tts_client.generate() finished {pc() - generate_start} sec"
        )  # TODO: delete
    except Exception as ex:
        logger.error(f"{type(ex)}: {ex}")
        return ex

    if audio_bytes:
        save_start = pc()  # TODO: delete

        target_audio.write_bytes(audio_bytes)
        logger.info(request.format_log(str(ref_audio), str(target_audio)))

        logger.info(f"Save target_audio {pc() - save_start} sec")  # TODO: delete
    else:
        logger.warning(
            f"Empty response with request: {request.format_log(str(ref_audio), str(target_audio))}"
        )
        return

    logger.info(f"TOTAL remote conversion {pc() - total} sec")  # TODO: delete


def streaming_conversion(
    limit: Optional[int] = None,
    start_with: Optional[int] = None,
    change_dir: Optional[str] = None,
):
    total_start = pc()  # TODO: delete
    logger.info("========== START STREAMING CONVERSION ==========")  # TODO: delete

    data = get_all_subs_iter(batch_size=100)

    for i, sub in enumerate(data, start=1):
        subtitle_start = pc()  # TODO: delete
        logger.info(f"[{sub.id}] processing started")  # TODO: delete

        if limit and i >= limit:
            break
        if start_with and i < start_with:
            continue
        logger.info(f"Sub #{i}")

        ref_text = sub.en_sub
        target_text = sub.ru_accent
        for ogg in sub.oggs:
            ref_audio = Path(ogg.wav_en_path)
            target_audio = Path(ogg.wav_ru_path)

            try:
                audio_start = pc()  # TODO: delete
                logger.info(
                    f"[{sub.id}] convert_audio_with_remote_session() started"
                )  # TODO: delete

                convert_audio_with_remote_session(
                    sub_id=sub.id,
                    ref_text=ref_text,
                    target_text=target_text,
                    ref_audio=ref_audio,
                    target_audio=target_audio,
                    change_dir=change_dir,
                )

                logger.info(
                    f"[{sub.id}] convert_audio_with_remote_session() finished {pc() - audio_start} sec"
                )  # TODO: delete
            except Exception as ex:
                logger.exception(ex)
                continue

        logger.info(f"[{sub.id}] TOTAL {pc() - subtitle_start} sec")  # TODO: delete
    logger.info(
        f"========== TOTAL STREAM {pc() - total_start} sec =========="
    )  # TODO: delete


# @inject_tts
# def convert_audio_with_remote_session_old(
#     tts_client: TTSClient,
#     sub: SubDTO,
#     change_dir: Optional[str] = None,
# ):
#     ref_text = sub.en_sub
#     target_text = sub.ru_accent
#     for ogg in sub.oggs:
#         ref_audio = Path(ogg.wav_en_path)
#         target_audio = Path(ogg.wav_ru_path)
#
#         if change_dir:
#             new_parts = [
#                 f"ru_voice_wav_{change_dir}" if part == "ru_voice_wav" else part
#                 for part in target_audio.parts
#             ]
#             target_audio = Path(*new_parts)
#
#         if target_audio.exists():
#             logger.warning(f"file {str(target_audio)} is exists")
#             continue
#         if not target_text:
#             logger.warning(f"target_text in id={sub.id} is None")
#             continue
#
#         target_audio.parent.mkdir(parents=True, exist_ok=True)
#
#         request = TTSRequestDTO(
#             ref_text=ref_text,
#             gen_text=target_text,
#         )
#         try:
#             audio_bytes = tts_client.generate(ref_audio=ref_audio, request=request)
#         except Exception as ex:
#             logger.error(f"{type(ex)}: {ex}")
#             continue
#
#         if audio_bytes:
#             target_audio.write_bytes(audio_bytes)
#             logger.info(request.format_log(str(ref_audio), str(target_audio)))
#         else:
#             logger.warning(
#                 f"Empty response with request: {request.format_log(str(ref_audio), str(target_audio))}"
#             )


# def convert_audio_en_to_ru(data: dict):
#     """
#     Генерирует русскоязычные аудиофайлы с использованием модели F5-TTS.
#
#     Для каждого элемента словаря `data` функция берет эталонное аудио
#     (`wav_en_path`) и соответствующий английский текст (`en_sub`),
#     после чего выполняет синтез речи на русском языке и сохраняет
#     результат в файл, указанный в `wav_ru_path`.
#
#     Если целевой аудиофайл уже существует, генерация для данного
#     элемента пропускается.
#
#     Args:
#         data (dict): Словарь вида:
#             {
#                 "<key>": {
#                     "wav_en_path": "<путь к эталонному аудио>",
#                     "en_sub": "<английский текст>",
#                     "ru_sub": "<русский текст>",
#                     "wav_ru_path": "<путь для сохранения результата>",
#                     ...
#                 },
#                 ...
#             }
#
#     Returns:
#         None
#
#     Side Effects:
#         - Загружает модель F5-TTS.
#         - Создает отсутствующие директории для выходных файлов.
#         - Генерирует и сохраняет WAV-файлы с частотой дискретизации 24000 Гц.
#         - Записывает аудиоданные на диск.
#
#     Notes:
#         - В текущей реализации для синтеза используется тестовая строка,
#           переданная в параметр `gen_text`, а не значение поля `ru_sub`.
#         - При включенном режиме DEBUG обрабатывается только первый
#           подходящий элемент словаря.
#         - Ключ `"nothing"` пропускается.
#     """
#     import soundfile as sf
#     from f5_tts.api import F5TTS
#
#     DEBUG = 0
#     tts = F5TTS(
#         ckpt_file=SAFETENSORS_MISHA,
#         vocab_file=VOCAB_MISHA,
#         device="cpu",
#     )
#
#     len_data = len(data)
#     for i, (key, value) in enumerate(data.items(), start=1):
#         if DEBUG and i == 30:
#             break
#         if key == "nothing":
#             continue
#
#         ref_audio = value.get("wav_en_path")
#         ref_text = value.get("en_sub")  # важно для качества
#         target_audio = Path(value.get("wav_ru_path"))
#         target_text = value.get("ru_sub_accent")
#
#         if target_audio.exists():
#             continue
#
#         print(f"\n\n{i}/{len_data}")
#         if not target_text:
#             print("No ru_sub_accent")
#             append_txt(KEYS_WITHOUT_RUSUB, key)
#             continue
#
#         target_audio.parent.mkdir(parents=True, exist_ok=True)
#
#         wav, sr, spec = tts.infer(
#             ref_file=ref_audio,
#             ref_text=ref_text,
#             gen_text=target_text,
#         )
#         sf.write(target_audio, wav, 24000)


if __name__ == "__main__":
    pass
