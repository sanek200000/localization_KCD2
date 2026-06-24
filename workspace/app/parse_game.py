from pathlib import Path
from zipfile import ZipFile
from tqdm import tqdm
from helper import GAME_FOLDER, TEMP_PATH, append_json, append_txt

DATA_FOLDER = GAME_FOLDER.joinpath("Data")
PAKS_FOLDER = TEMP_PATH.joinpath("paks")

PAKS_TO_CHECK = [
    "Tables.pak",  # главный кандидат
    "Scripts.pak",  # Storm, диалоги, роли NPC, логика
    "IPL_GameData.pak",  # игровые данные, квесты, сущности
    "Sounds.pak",  # voice events, soundbanks, audio mappings
    "Cinematics.pak",  # сюжетные сцены и диалоговые треки
    # второй эшелон
    "Animations.pak",  # facial/dialog fragments, mannequin
    "Characters.pak",  # сущности персонажей
]


def list_all_files(folder: Path = DATA_FOLDER):
    """
    Рекурсивно собирает список файлов в указанной директории и
    сохраняет результат в JSON-файл.

    Для обычных файлов в результат сохраняется полный путь.
    Для файлов с расширением `.pak` дополнительно извлекается список
    содержащихся в архиве файлов.

    Args:
        folder (Path, optional): Корневая директория для обхода.
            По умолчанию используется `DATA_FOLDER`.

    Returns:
        None

    Side Effects:
        - Выполняет рекурсивный обход файловой системы.
        - Открывает PAK-архивы для чтения.
        - Создает JSON-файл со списком найденных файлов.
        - Выводит прогресс и итоговую статистику в консоль.

    Notes:
        - Каталоги пропускаются.
        - Для PAK-файлов в результат сохраняется словарь вида:

          {
              "<путь к pak>": [
                  "<файл 1>",
                  "<файл 2>",
                  ...
              ]
          }

        - При включенном режиме DEBUG обрабатываются только первые
          10 элементов.
    """
    DEBUG = 0
    result = list()
    save_result_path = TEMP_FOLDER.joinpath(
        f"list_files_from_folder__{folder.name}.json"
    )

    for i, file in enumerate(folder.rglob("*")):
        if DEBUG and i == 10:
            break
        if file.is_dir():
            continue
        if i % 10 == 0:
            print(i)

        if file.suffix == ".pak":
            with ZipFile(file, "r") as archive:
                files_in_pak = archive.namelist()
                result.append({str(file): files_in_pak})
        else:
            result.append(str(file))

    append_json(save_result_path, result)
    print("count len: ", len(result))


def list_one_pak_file(folder: Path = DATA_FOLDER, pak_name: str = "000"):
    """
    Извлекает список содержимого указанного PAK-архива и сохраняет
    его в текстовый файл.

    Выполняет рекурсивный поиск файлов в директории `folder`.
    Если путь к файлу заканчивается строкой `pak_name`,
    архив открывается и список его содержимого записывается
    в отдельный TXT-файл.

    Args:
        folder (Path, optional): Корневая директория для поиска.
            По умолчанию используется `DATA_FOLDER`.
        pak_name (str, optional): Имя или суффикс искомого
            PAK-файла. По умолчанию `"000"`.

    Returns:
        None

    Side Effects:
        - Выполняет рекурсивный обход файловой системы.
        - Открывает PAK-архивы для чтения.
        - Создает или перезаписывает текстовые файлы
          в каталоге `PAKS_FOLDER`.

    Notes:
        Для каждого найденного архива создается текстовый файл,
        содержащий полный список файлов внутри архива, по одному
        имени на строку.
    """

    for i, file in enumerate(folder.rglob("*")):
        if file.is_dir():
            continue

        if str(file).endswith(pak_name):
            save_result_path = PAKS_FOLDER.joinpath(
                f"{str(file.parent / file.name).replace('/', '_')}.txt"
            )
            save_result_path.unlink(missing_ok=True)

            with ZipFile(file, "r") as archive:
                append_txt(save_result_path, "\n".join(archive.namelist()))


if __name__ == "__main__":
    pass

    for file_name in tqdm(PAKS_TO_CHECK, desc="files: "):
        list_one_pak_file(pak_name=file_name)

    # list_all_files()
