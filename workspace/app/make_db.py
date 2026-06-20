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
    Выполняет рекурсивный поиск OGG-файлов, формирует записи для базы
    данных и сохраняет индекс найденных файлов.

    Для каждого найденного файла:

    - Проверяет уникальность имени файла без расширения.
    - Вычисляет связанные пути к WAV- и русскоязычным OGG-файлам.
    - Создает объект `OggAdd`.
    - Добавляет запись в базу данных через функцию `add_ogg`.
    - Добавляет информацию о файле в локальный индекс.

    После завершения обработки индекс сохраняется в бинарном и JSON
    форматах, а также записывается статистика по количеству найденных
    файлов.

    Args:
        folder (Path, optional): Каталог, в котором выполняется
            рекурсивный поиск файлов с расширением ``.ogg``.
            По умолчанию используется `EN_VOICE_OGG_PATH`.

    Returns:
        None

    Side Effects:
        - Выполняет рекурсивный обход файловой системы.
        - Создает записи в базе данных.
        - Создает или перезаписывает файлы индекса.
        - Создает JSON-представление индекса.
        - Записывает статистику в файл `counts.txt`.
        - Выводит сообщения об ошибках в консоль.

    Raises:
        Любые исключения, возникающие при работе с файловой системой,
        базой данных или сериализацией, не перехватываются и
        пробрасываются вызывающему коду.

    Notes:
        - В качестве идентификатора используется имя файла без
          расширения (`Path.stem`).
        - Значение поля `hash` формируется из последних 15 символов
          имени файла.
        - При обнаружении дублирующегося имени файла обработка
          прерывается.
        - При включенном режиме DEBUG обрабатываются только первые
          12 найденных файлов.
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

        wav_en_path, ogg_ru_path, wav_ru_path = replace_ogg_path(str(ogg))
        row = OggAdd(
            hash=ogg_stem[-15:],
            name=ogg_stem,
            ogg_en_path=str(ogg),
            wav_en_path=wav_en_path,
            ogg_ru_path=ogg_ru_path,
            wav_ru_path=wav_ru_path,
        )
        add_ogg(data=row)

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


def replace_ogg_path(ogg_path) -> tuple[str, str, str]:
    """
    Формирует связанные пути для WAV-версии исходного аудио и
    русскоязычных аудиофайлов на основе пути к английскому OGG-файлу.

    Выполняет замену каталогов в исходном пути и при необходимости
    изменяет расширение файла на ``.wav``.

    Args:
        ogg_path (str): Путь к английскому OGG-файлу, расположенному
            в каталоге `en_voice_ogg`.

    Returns:
        tuple[str, str, str]:
            Кортеж из трех путей:

            - `wav_en_path` — путь к английскому WAV-файлу;
            - `ogg_ru_path` — путь к русскому OGG-файлу;
            - `wav_ru_path` — путь к русскому WAV-файлу.

    Examples:
        >>> replace_ogg_path(
        ...     "/data/en_voice_ogg/dialog/test_123.ogg"
        ... )
        (
            "/data/en_voice_wav/dialog/test_123.wav",
            "/data/ru_voice_ogg/dialog/test_123.ogg",
            "/data/ru_voice_wav/dialog/test_123.wav"
        )

    Notes:
        Функция предполагает, что входной путь содержит подстроку
        `"en_voice_ogg"`. Если структура каталогов отличается,
        результат может быть некорректным.
    """
    wav_en_path = str(
        Path(ogg_path.replace("en_voice_ogg", "en_voice_wav")).with_suffix(".wav")
    )
    ogg_ru_path = ogg_path.replace("en_voice_ogg", "ru_voice_ogg")
    wav_ru_path = str(
        Path(ogg_path.replace("en_voice_ogg", "ru_voice_wav")).with_suffix(".wav")
    )
    return wav_en_path, ogg_ru_path, wav_ru_path


def add_entry_to_subs_dict(data: dict, key: str, ogg_path: str):
    """
    Дополняет существующую запись словаря путями к аудиофайлам.

    Для указанного ключа извлекает запись из словаря `data` и, если
    она существует, добавляет в нее пути к английским и русским
    аудиофайлам в форматах OGG и WAV.

    Пути формируются на основе исходного пути к английскому OGG-файлу
    с помощью функции `replace_ogg_path`.

    Args:
        data (dict): Словарь с данными субтитров или аудиозаписей.
        key (str): Ключ записи, которую необходимо дополнить.
        ogg_path (str): Путь к английскому OGG-файлу.

    Returns:
        None

    Side Effects:
        Изменяет содержимое словаря `data`:
        добавляет или обновляет поля:

        - `ogg_en_path`
        - `wav_en_path`
        - `ogg_ru_path`
        - `wav_ru_path`

    Notes:
        Если запись с указанным ключом отсутствует в словаре,
        функция не выполняет никаких действий.
    """
    wav_en_path, ogg_ru_path, wav_ru_path = replace_ogg_path(ogg_path)

    if sub_entry := data.get(key):
        sub_entry["ogg_en_path"] = ogg_path
        sub_entry["wav_en_path"] = wav_en_path
        sub_entry["ogg_ru_path"] = ogg_ru_path
        sub_entry["wav_ru_path"] = wav_ru_path


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
