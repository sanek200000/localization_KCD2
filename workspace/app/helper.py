import json
import marshal
from pathlib import Path


def append_txt(file_path: Path | str, text: str):
    with open(file_path, "a", encoding="utf-8") as file:
        print(text, file=file)


def load_json(file_path: Path | str) -> list[str] | dict:
    """
    Загружает данные из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу.

    Returns:
        Содержимое JSON-файла в виде списка или словаря в зависимости
        от структуры данных в файле.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def append_json(file_path: Path | str, data: dict | list) -> None:
    """
    Сохраняет словарь в JSON-файл.

    Записывает переданные данные в файл в формате JSON с отступами
    для удобства чтения и без экранирования не-ASCII символов.

    Args:
        file_path: Путь к файлу для записи.
        data: Словарь с данными для сериализации.

    Returns:
        None.

    Raises:
        OSError: Если не удалось создать или записать файл.
        TypeError: Если объект содержит значения, не поддерживающие
            JSON-сериализацию.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def append_marshal(file_path: Path | str, data: list | dict) -> None:
    """
    Сериализует данные и сохраняет их в бинарный файл с использованием
    модуля marshal.

    Args:
        file_path: Путь к файлу для записи.
        data: Список или словарь, подлежащий сериализации.

    Returns:
        None.

    Raises:
        OSError: Если не удалось создать или записать файл.
        ValueError: Если объект содержит данные, не поддерживаемые
            модулем marshal.

    Notes:
        Формат marshal предназначен главным образом для внутренних нужд
        Python и не гарантирует совместимость между различными версиями
        интерпретатора.
    """
    with open(file_path, "wb") as file:
        marshal.dump(data, file)


def load_marshal(file_path: Path | str) -> dict:
    """
    Десериализует данные из бинарного файла, сохранённого через marshal.

    Args:
        file_path: Путь к бинарному файлу с данными marshal.

    Returns:
        Объект типа dict, восстановленный из файла.

    Raises:
        FileNotFoundError: Если файл не найден.
        EOFError: Если файл повреждён или неожиданно обрывается.
        ValueError: Если содержимое файла не может быть десериализовано
            через marshal.
        TypeError: Если структура данных несовместима с ожидаемым типом.

    Notes:
        Модуль marshal не предназначен для долгосрочного хранения данных
        и не гарантирует совместимость между версиями Python.
    """
    with open(file_path, "rb") as file:
        return marshal.load(file)


if __name__ == "__main__":
    pass
