import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from helper import load_marshal, append_txt

DB_WITH_FILES_PATHES = Path("./temp/db_with_pathes.bin")
KEYS_WITHOUT_OGG = Path("./temp/keys_without_oggs.txt")


def convert_ogg_to_wav_onethread(data: dict):
    """
    Конвертирует OGG-файлы в WAV-файлы в однопоточном режиме.

    Рекурсивно обходит словарь с описанием аудиофайлов, извлекает пути
    к исходным OGG-файлам и соответствующим WAV-файлам, после чего
    выполняет конвертацию через утилиту FFmpeg.

    Если WAV-файл уже существует, обработка записи пропускается.

    Args:
        data (dict): Словарь с данными аудиофайлов.

    Returns:
        None

    Side Effects:
        - Создает отсутствующие директории.
        - Запускает внешние процессы FFmpeg.
        - Создает WAV-файлы на диске.
        - Выводит диагностическую информацию в консоль.

    Raises:
        subprocess.CalledProcessError:
            Если FFmpeg завершился с ошибкой.

    Notes:
        Записи с ключом `"nothing"` обрабатываются рекурсивно как
        вложенные словари.
    """
    DEBUG = 0

    for i, (key, value) in enumerate(data.items()):
        if DEBUG and i == 30:
            break
        if key == "nothing":
            convert_ogg_to_wav_onethread(data.get("nothing"))
            # continue

        print(key, value, sep="\n", end="\n\n")
        input_ogg = Path(value.get("ogg_en_path")).resolve()
        output_wav = Path(value.get("wav_en_path")).resolve()
        if not output_wav.exists():
            output_wav.parent.mkdir(parents=True, exist_ok=True)
            command = (
                f"ffmpeg -i {input_ogg} -ac 1 -ar 24000 -c:a pcm_s16le {output_wav}",
            )
            subprocess.run(command, shell=True, check=True)


def process_item(item: dict):
    """
    Обрабатывает одну запись аудиофайла и выполняет конвертацию
    OGG → WAV при необходимости.

    Args:
        item (tuple[str, dict]): Кортеж из ключа записи и словаря
            с путями к аудиофайлам.

    Returns:
        None

    Side Effects:
        - Создает отсутствующие директории.
        - Запускает FFmpeg для конвертации аудио.
        - Создает WAV-файл на диске.
        - Записывает ключ в файл `KEYS_WITHOUT_OGG`, если данные
          о путях отсутствуют.

    Raises:
        subprocess.CalledProcessError:
            Если FFmpeg завершился с ошибкой.
    """
    key, value = item

    # input_ogg = Path(value["ogg_en_path"]).resolve()
    # output_wav = Path(value["wav_en_path"]).resolve()
    try:
        input_ogg = Path(value.get("ogg_en_path")).resolve()
        output_wav = Path(value.get("wav_en_path")).resolve()
    except:
        append_txt(KEYS_WITHOUT_OGG, key)
        return

    if output_wav.exists():
        return

    output_wav.parent.mkdir(parents=True, exist_ok=True)
    command = f"ffmpeg -i {input_ogg} -ac 1 -ar 24000 -c:a pcm_s16le {output_wav}"
    subprocess.run(command, shell=True, check=True)


def iter_items(data: dict):
    """
    Рекурсивно обходит словарь аудиоданных и возвращает записи
    в виде последовательности пар ключ-значение.

    Вложенные словари, расположенные под ключом `"nothing"`,
    обходятся рекурсивно.

    Args:
        data (dict): Словарь с аудиоданными.

    Yields:
        tuple[str, dict]: Ключ записи и связанный словарь данных.
    """
    for key, value in data.items():
        if key == "nothing":
            yield from iter_items(value)
        else:
            yield key, value


def convert_ogg_to_wav(data: dict):
    """
    Конвертирует OGG-файлы в WAV-файлы в многопоточном режиме.

    Для обработки используется пул потоков `ThreadPoolExecutor`.
    Каждая запись передается в функцию `process_item`, которая
    выполняет конвертацию через FFmpeg.

    Args:
        data (dict): Словарь с данными аудиофайлов.

    Returns:
        None

    Side Effects:
        - Создает WAV-файлы на диске.
        - Создает отсутствующие директории.
        - Запускает несколько процессов FFmpeg параллельно.
        - Может записывать ключи проблемных записей в файл
          `KEYS_WITHOUT_OGG`.

    Notes:
        Максимальное количество одновременно работающих потоков
        ограничено значением `max_workers=20`.
    """
    with ThreadPoolExecutor(max_workers=20) as executor:
        list(executor.map(process_item, iter_items(data)))


if __name__ == "__main__":
    pass

    data = load_marshal(DB_WITH_FILES_PATHES)
    convert_ogg_to_wav(data)
