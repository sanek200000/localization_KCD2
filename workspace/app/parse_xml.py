from app.config import LOCALIZATION_PATH, TEMP_PATH
from helper import append_json, append_txt, load_json, append_marshal
from pathlib import Path
import xml.etree.ElementTree as ET
from tqdm import tqdm

RU_DILOG_XML = LOCALIZATION_PATH.joinpath("/Russian_xml/text_ui_dialog.xml")
EN_DILOG_XML = LOCALIZATION_PATH.joinpath("/English_xml/text_ui_dialog.xml")
RU_XMLS_FOLDER = LOCALIZATION_PATH.joinpath("Russian_xml")
EN_XMLS_FOLDER = LOCALIZATION_PATH.joinpath("English_xml")

JSON_DATA_FILE = TEMP_PATH.joinpath("from_xml.json")
RU_SUB_KEYS_LIST = TEMP_PATH.joinpath("from_Russian_xml_xml.json")


def parse_xml(xml_path: Path, data: dict, empty_keys: list):
    """
    Парсит XML-файл и заполняет словарь данными из элементов Row.

    Для каждой строки XML извлекает ключ из первого элемента Cell,
    формирует вторичный ключ как часть строки после первого символа "_"
    и сохраняет данные о переводах в словарь.

    Args:
        xml_path: Путь к XML-файлу.
        data: Словарь для заполнения данными. Для каждого ключа создаётся
            запись следующего формата:
            {
                "key": <исходный ключ>,
                "en_sub": <английский текст>,
                "ru_sub": <русский текст>
            }

    Returns:
        None.

    Notes:
        При обнаружении дублирующегося ключа выводит сообщение об ошибке
        и прекращает обработку файла.
    """
    DEBUG = 0

    # data = dict()
    # empty_keys = list()

    tree = ET.parse(xml_path)
    root = tree.getroot()

    for i, row in enumerate(tqdm(root.findall("Row"), desc="Parsing XML: ")):
        if DEBUG and i == 10:
            break

        cells = row.findall("Cell")
        key, en_sub, second_sub = [cell.text for cell in cells]
        row_data = f"{key = } || {en_sub = } || {second_sub = }"

        if data.get(key):
            print(f"Error: Key {key} repeat!!! \nOriginal dict: {data.get(key)}")
            print(row_data)
            break

        if en_sub == None and second_sub == None:
            # print("Empty element:")
            empty_keys.append(row_data)
        else:
            data[key] = {
                "en_sub": en_sub,
                "ru_sub": second_sub,
            }


def move_by_xmls(folder: Path):
    """
    Собирает данные локализации из XML-файлов и сохраняет их в бинарный файл.

    Рекурсивно обходит каталог с XML-файлами, находит файл локализации
    `text_ui_dialog.xml`, извлекает из него данные с помощью функции
    `parse_xml()` и сохраняет результат в бинарный файл через
    `append_marshal()`.

    Returns:
        None.

    Notes:
        Данные накапливаются в словаре `data`, который передаётся в
        `parse_xml()` для заполнения.

        В текущей реализации обрабатывается только файл
        `localization/Russian_xml/text_ui_dialog.xml`.

        Сохранение в JSON предусмотрено, но закомментировано.
    """
    data = dict()
    empty_keys = list()

    data_file_path = Path(f"./temp/from_{folder.name}_xml.bin")
    empty_keys_file_path = Path(f"./temp/empty_keys_from_{folder.name}.txt")
    data_file_path.unlink(missing_ok=True)
    empty_keys_file_path.unlink(missing_ok=True)

    xmls = folder.rglob("*.xml")
    for xml in xmls:
        if not str(xml).endswith("text_ui_dialog.xml"):
            continue

        print(xml)
        parse_xml(xml, data, empty_keys)

    append_marshal(data_file_path, data)
    append_json(data_file_path.with_suffix(".json"), data)

    append_txt(empty_keys_file_path, "\n".join(empty_keys))
    append_txt(
        "./temp/counts.txt",
        f"|{folder}| entries: {len(data)}, empties: {len(empty_keys)}",
    )


def list_all_subs():
    """
    Загружает данные локализации из JSON-файла, выводит список ключей
    и сохраняет данные в бинарный файл.

    Извлекает все ключи верхнего уровня из словаря, загруженного из
    файла `from_xml.json`, выводит их в консоль и сериализует исходные
    данные в файл `subs.bin` с помощью `append_marshal()`.

    Returns:
        None.

    Notes:
        Список ключей сохраняется только в локальную переменную `result`
        и выводится на экран. В бинарный файл записывается исходный
        словарь `data`, а не список ключей.
    """
    data = load_json(JSON_DATA_FILE)

    result = list()
    for key in data:
        result.append(key)

    append_marshal("./subs.bin", data)
    print(result)


def check_ru_sub_keys(keys: list[str], n: int):
    DEBUG = 0
    data = dict()
    is_error = False

    for i, key in enumerate(keys, start=1):
        if DEBUG and i == 10:
            break

        hash = key[-n:]
        if data.get(hash):
            is_error = 1
            print("Error: ", i, hash, data.get(hash), key, sep=";")
            n += 1
            check_ru_sub_keys(keys, n)
            break

        data[hash] = key

    if not is_error:
        print(f"{n = }")


if __name__ == "__main__":
    pass

    keys_list = load_json(RU_SUB_KEYS_LIST)
    check_ru_sub_keys(keys_list, 4)

    # list_all_subs()
    # move_by_xmls(RU_XMLS_FOLDER)
