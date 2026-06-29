from pydantic import ValidationError

from app.config import TEMP_PATH
from app.schemas.subs import SubAddDTO
from app.api.subs import add_sub
from helper import load_marshal
from ruaccent import RUAccent

DB_WITH_FILES_PATHES = TEMP_PATH.joinpath("db_with_pathes.bin")
DB_WITH_FILES_PATHES_AND_ACCENT = TEMP_PATH.joinpath("db_with_pathes_and_accent.bin")
DB_ERROR_ACCENT = TEMP_PATH.joinpath("db_error_accent.bin")

accentizer = RUAccent()
accentizer.load(omograph_model_size="turbo3.1", use_dictionary=True, tiny_mode=False)


def convert_ru_sub(text: str):
    """
    Расставляет ударения в русском тексте с использованием модели
    RUAccent.

    Args:
        text (str): Русскоязычный текст для обработки.

    Returns:
        str: Текст с автоматически расставленными ударениями.

    Raises:
        Exception: Если при обработке текста возникла ошибка
            в библиотеке RUAccent.

    Notes:
        Перед обработкой текст очищается от пробелов в начале
        и конце строки с помощью `strip()`.
    """
    try:
        accent_text = accentizer.process_all(text.strip())
    except Exception as ex:
        raise Exception(ex)

    return accent_text


def add_accents(data: dict):
    """
    Добавляет ударения ко всем русскоязычным субтитрам в словаре.

    Для каждой записи извлекает текст из поля `ru_sub`,
    обрабатывает его функцией `convert_ru_sub()` и сохраняет
    результат в поле `ru_sub_accent`.

    Записи с ключом `"nothing"` пропускаются.

    Args:
        data (dict): Словарь с данными субтитров.

    Returns:
        dict: Словарь ошибок обработки.

    Notes:
        В текущей реализации словарь ошибок всегда остается пустым,
        поскольку обработка исключений выполняется внутри функции
        `convert_ru_sub()`.
    """
    DEBUG = 0

    error_keys = dict()
    for i, (key, value) in enumerate(data.items()):
        if DEBUG and i == 3:
            break
        if key == "nothing":
            continue

        text = value.get("ru_sub")
        print(text)

        accent_text = convert_ru_sub(text)
        value["ru_sub_accent"] = accent_text

    return error_keys


def fill_subs():
    """
    Загружает субтитры из промежуточного хранилища и сохраняет их
    в базу данных.

    Для каждой записи извлекает ключ субтитра, оригинальный текст,
    перевод и версию текста с ударениями, после чего формирует
    объект `SubAddDTO` и передает его в API-функцию `add_sub()`.

    Записи с ключом `"nothing"` пропускаются.

    Returns:
        None

    Raises:
        Exception: Если структура записи не содержит необходимых
            полей или содержит некорректные данные.

    Side Effects:
        - Загружает данные из файла
          `DB_WITH_FILES_PATHES_AND_ACCENT`.
        - Создает объекты `SubAddDTO`.
        - Сохраняет записи в базе данных через `add_sub()`.
        - Выводит диагностическую информацию в консоль при ошибках
          валидации или обработки данных.

    Notes:
        В качестве ключа используется последние 15 символов поля
        `value["key"]`.
    """
    DEBUG = 0
    data: dict = load_marshal(DB_WITH_FILES_PATHES_AND_ACCENT)

    for i, (key, value) in enumerate(data.items()):
        if DEBUG and i == 10:
            break
        if key == "nothing":
            continue

        try:
            key_sub = value.get("key")[-15:]
            en_sub = value.get("en_sub")
            ru_sub = value.get("ru_sub")
            ru_accent = value.get("ru_sub_accent")
        except Exception as ex:
            [print(f"{k}:\t{v}") for k, v in value.items()]
            raise Exception(ex)

        try:
            sub_data = SubAddDTO(
                key=key_sub,
                en_sub=en_sub,
                ru_sub=ru_sub,
                ru_accent=ru_accent,
            )
        except ValidationError as ex:
            [print(f"{k}:\t{v}") for k, v in value.items()]

        add_sub(data=sub_data)


if __name__ == "__main__":
    pass

    # data = load_marshal(DB_WITH_FILES_PATHES)
    # error_result = add_accents(data)
    # append_marshal(DB_WITH_FILES_PATHES_AND_ACCENT, data)
    # append_marshal(DB_ERROR_ACCENT, error_result)

    data = load_marshal(DB_ERROR_ACCENT)
    print(data, len(data), sep="\n\n")
