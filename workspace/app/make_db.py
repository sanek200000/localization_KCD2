from pathlib import Path
from tqdm import tqdm
from app.api.oggs import add_ogg
from app.config import LOCALIZATION_PATH, TEMP_PATH
from app.helper import append_json, append_marshal, append_txt, load_marshal
from app.schemas.oggs import OggAdd

EN_VOICE_OGG_PATH = LOCALIZATION_PATH.joinpath("en_voice_ogg").resolve()
EN_VOICE_WAV_PATH = LOCALIZATION_PATH.joinpath("en_voice_wav").resolve()
RU_VOICE_OGG_PATH = LOCALIZATION_PATH.joinpath("ru_voice_ogg").resolve()

SOURCE_JSON = TEMP_PATH.joinpath("/from_xml.json").resolve()
REVERSE_INDEX_FOR_SUB = TEMP_PATH.joinpath("/reverse_index_for_sub.bin").resolve()
OGGS_DICT = TEMP_PATH.joinpath("/oggs.bin").resolve()
SUBS_DICT = TEMP_PATH.joinpath("/subs.bin").resolve()
DB_WITH_FILES_PATHES = TEMP_PATH.joinpath("/db_with_pathes.bin").resolve()


def list_all_oggs(folder: Path = EN_VOICE_OGG_PATH):
    """
    Рекурсивно собирает список всех OGG-файлов в указанной директории
    и сохраняет результат в бинарный файл.

    Функция обходит каталог `folder`, находит все файлы с расширением
    ``.ogg`` и формирует словарь, где ключом является имя файла без
    расширения, а значением — полный путь к файлу.

    После завершения обхода словарь сериализуется и сохраняется
    в файл внутри директории `TEMP_PATH`. Также в текстовый лог
    записывается количество найденных файлов.

    Args:
        folder (Path, optional): Корневая директория для поиска OGG-файлов.
            По умолчанию используется `EN_VOICE_OGG_PATH`.

    Returns:
        None

    Side Effects:
        - Удаляет существующий файл результата перед созданием нового.
        - Выполняет рекурсивный обход файловой системы.
        - Сохраняет словарь путей через функцию `append_marshal`.
        - Добавляет запись в файл статистики через функцию `append_txt`.
        - Выводит сообщение об ошибке при обнаружении дублирующихся имен файлов.

    Notes:
        - Ключом словаря используется только имя файла (`Path.stem`).
          Если в разных подкаталогах встречаются файлы с одинаковыми
          именами, функция завершает обработку после вывода сообщения
          об ошибке.
        - При включенном режиме DEBUG обрабатываются только первые
          10 найденных файлов.
    """
    DEBUG = 1
    save_file_path = TEMP_PATH.joinpath(f"list_oggs_from__{folder.name}.bin")
    save_file_path.unlink(missing_ok=True)

    data = dict()
    for i, ogg in enumerate(tqdm(folder.rglob("*.ogg"), desc="OGG files: ")):
        if DEBUG and i == 12:
            break

        ogg_stem = ogg.stem
        if data.get(ogg_stem):
            print(
                f"Error: Key {ogg_stem} repeat!!! \nOriginal dict: {data.get(ogg_stem)}"
            )
            break

        data[ogg_stem] = str(ogg)

        row = OggAdd(hash=ogg_stem[-15:], name=ogg_stem, path=str(ogg))
        add_ogg(row)

    append_marshal(save_file_path, data)
    append_json(save_file_path.with_suffix(".json"), data)

    append_txt(
        "./temp/counts.txt",
        f"|{folder}| entries: {len(data)}",
    )


def reverse_index_for_sub():
    """
    Строит обратный индекс для субключей на основе словаря SUBS_DICT.

    Функция загружает данные из бинарного файла SUBS_DICT и для каждого ключа
    формирует все возможные суффиксы (sub-stems), разделённые символом "_".
    Каждый такой суффикс индексируется в словарь stem_to_key.

    Логика обработки:
        - Для каждого ключа выполняется разбиение по "_"
        - Генерируются все возможные хвостовые подстроки (suffixes)
        - Если суффикс уже встречался, он помечается как неоднозначный (None)
        - Если встречается впервые, сохраняется соответствующий исходный ключ

    Args:
        None.

    Returns:
        None.

    Side Effects:
        - Периодически выводит прогресс обработки (каждые 1000 ключей)
        - Сохраняет построенный обратный индекс в REVERSE_INDEX_FOR_SUB

    Notes:
        - При коллизиях значение ключа в индексе устанавливается в None,
          что означает неоднозначное соответствие.
        - Используется стратегия reverse suffix indexing для ускорения
          последующего поиска по частичным строкам.
        - Переменная DEBUG ограничивает обработку первых элементов.
    """
    DEBUG = 0
    data = load_marshal(SUBS_DICT)
    stem_to_key = dict()

    for i, key in enumerate(data):
        if DEBUG and i == 3:
            break
        if i % 1000 == 0:
            print(i)

        parts = key.split("_")

        for i in range(len(parts)):
            stem = "_".join(parts[i:])

            if stem in stem_to_key:
                stem_to_key[stem] = None
            else:
                stem_to_key[stem] = key

    append_marshal(REVERSE_INDEX_FOR_SUB, stem_to_key)


def add_entry_to_subs_dict(data: dict, key: str, ogg_path: str):
    """
    Дополняет запись в словаре SUBS_DICT путями к аудиофайлам (OGG/WAV)
    для английской и русской локализаций.

    Функция модифицирует существующую запись в словаре `data`, добавляя
    производные пути к аудиофайлам на основе входного пути OGG.

    Формируемые поля:
        - ogg_en_path: исходный английский OGG-путь
        - wav_en_path: соответствующий WAV-путь (en_voice_ogg → en_voice_wav)
        - ogg_ru_path: русская версия OGG-пути (en_voice_ogg → ru_voice_ogg)
        - wav_ru_path: русская WAV-версия (en_voice_ogg → ru_voice_wav)

    Args:
        data: Словарь субтитров/записей, содержащий ключ `key`.
        key: Ключ записи, которую необходимо дополнить.
        ogg_path: Путь к английскому OGG-файлу.

    Returns:
        None.

    Notes:
        - Функция предполагает строго заданную структуру путей проекта.
        - Все преобразования путей основаны на строковой замене,
          поэтому чувствительны к формату исходного пути.
        - Используется pathlib.Path только для преобразования расширения WAV.
    """
    sub_entry = data.get(key)
    sub_entry["ogg_en_path"] = ogg_path
    sub_entry["wav_en_path"] = str(
        Path(ogg_path.replace("en_voice_ogg", "en_voice_wav")).with_suffix(".wav")
    )
    sub_entry["ogg_ru_path"] = ogg_path.replace("en_voice_ogg", "ru_voice_ogg")
    sub_entry["wav_ru_path"] = str(
        Path(ogg_path.replace("en_voice_ogg", "ru_voice_wav")).with_suffix(".wav")
    )


def add_oggs_to_subs_db():
    """
    Обогащает базу субтитров путями к аудиофайлам OGG/WAV и сохраняет результат.

    Функция объединяет данные из нескольких источников:
        - OGGS_DICT: словарь OGG-файлов (ключ → путь)
        - REVERSE_INDEX_FOR_SUB: обратный индекс для сопоставления субтитров
        - SUBS_DICT: база субтитров

    Для каждого OGG-файла:
        - извлекается stem (суффикс ключа)
        - выполняется поиск соответствующего ключа субтитров через reverse index
        - при успешном совпадении запись дополняется аудиопутями
        - при отсутствии совпадения запись помещается в раздел "nothing"

    Args:
        None.

    Returns:
        None.

    Side Effects:
        - Модифицирует структуру SUBS_DICT (в памяти)
        - Добавляет раздел "nothing" для несопоставленных OGG-файлов
        - Периодически выводит прогресс обработки
        - Сохраняет итоговую структуру в DB_WITH_FILES_PATHES через marshal

    Notes:
        - Используется эвристическое сопоставление через reverse index,
          построенный на суффиксах строк.
        - Структура данных чувствительна к формату ключей ogg_key.
        - При отсутствии совпадения создаются пустые записи в разделе "nothing".
        - Функция выполняет агрегацию данных между аудиофайлами и субтитрами.
    """
    DEBUG = 0
    oggs_dict = load_marshal(OGGS_DICT)
    reverse_index = load_marshal(REVERSE_INDEX_FOR_SUB)
    subs_dict = load_marshal(SUBS_DICT)
    subs_dict["nothing"] = dict()
    empty_subs = subs_dict["nothing"]

    for i, (ogg_key, ogg_path) in enumerate(oggs_dict.items(), 1):
        if DEBUG and i == 10:
            break
        if i % 1000 == 0:
            print(i)

        stem = ogg_key.split("_", 2)[-1]
        sub_key = reverse_index.get(stem)

        if sub_key:
            add_entry_to_subs_dict(subs_dict, sub_key, ogg_path)
            # print(i, subs_dict.get(sub_key))
        else:
            empty_subs[ogg_key] = dict()
            add_entry_to_subs_dict(empty_subs, ogg_key, ogg_path)
            # print(ogg_key, ogg_path)
            continue

    append_marshal(DB_WITH_FILES_PATHES, subs_dict)


if __name__ == "__main__":
    pass

    # list_all_oggs()

    file_name = Path("list_oggs_from__en_voice_ogg.bin")
    data = load_marshal(f"./temp/{file_name}")
    keys = list(data)
    append_json(TEMP_PATH / file_name.with_suffix(".json"), keys)
    # append_txt(f"./temp/{file_name.with_suffix('.txt')}", "\n".join(keys))

    # check_keys()
    # convert_ogg()
    # reverse_index_for_sub()
    # add_oggs_to_subs_db()
