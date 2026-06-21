#!/usr/bin/env python3

from pathlib import Path
from app.config import TEMP_PATH
from helper import append_marshal, load_marshal

DB_WITH_FILES_PATHES = TEMP_PATH.joinpath("db_with_pathes.bin")
DB_WITH_FILES_PATHES_AND_ACCENT = TEMP_PATH.joinpath("db_with_pathes_and_accent.bin")
DB_ERROR_ACCENT = TEMP_PATH.joinpath("db_error_accent.bin")


def add_accents(data: dict):
    """
    Добавляет ударения в русскоязычные субтитры с помощью библиотеки RUAccent.

    Функция проходит по всем элементам словаря `data`, извлекает текст из
    поля ``ru_sub``, расставляет ударения и сохраняет результат в поле
    ``ru_sub_accent`` соответствующего элемента. Элементы с ключом
    ``"nothing"`` пропускаются.

    В случае ошибки обработки текст сохраняется в словарь ошибок, который
    возвращается по завершении работы.

    Args:
        data (dict): Словарь вида:
            {
                "<key>": {
                    "ru_sub": "<текст на русском языке>",
                    ...
                },
                ...
            }

    Returns:
        dict: Словарь ошибок в формате:
            {
                "<key>": "<исходный текст из ru_sub>",
                ...
            }
        Содержит только записи, для которых не удалось выполнить
        расстановку ударений.

    Side Effects:
        - Добавляет поле ``ru_sub_accent`` в элементы словаря `data`.
        - Выводит в консоль исходный и обработанный текст.
        - Загружает и инициализирует модель RUAccent.

    Raises:
        Исключения, возникающие при обработке отдельных текстов,
        перехватываются внутри функции и не пробрасываются наружу.
    """
    from ruaccent import RUAccent

    DEBUG = 0

    accentizer = RUAccent()
    accentizer.load(
        omograph_model_size="turbo3.1", use_dictionary=True, tiny_mode=False
    )

    error_keys = dict()
    for i, (key, value) in enumerate(data.items()):
        if DEBUG and i == 3:
            break
        if key == "nothing":
            continue

        text = value.get("ru_sub")
        print(text)

        try:
            accent_text = accentizer.process_all(text)
            value["ru_sub_accent"] = accent_text
        except Exception as e:
            error_keys[key] = value.get("ru_sub")
            accent_text = None
            continue

        print(accent_text, end="\n\n")
        # [print(k, v) for k, v in value.items()]
        # print()

    return error_keys


if __name__ == "__main__":
    pass

    # data = load_marshal(DB_WITH_FILES_PATHES)
    # error_result = add_accents(data)
    # append_marshal(DB_WITH_FILES_PATHES_AND_ACCENT, data)
    # append_marshal(DB_ERROR_ACCENT, error_result)

    data = load_marshal(DB_ERROR_ACCENT)
    print(data, len(data), sep="\n\n")
