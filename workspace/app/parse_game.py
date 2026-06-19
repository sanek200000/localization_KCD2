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
