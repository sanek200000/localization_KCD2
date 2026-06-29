import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))

from app.config import APP_PATH
from app.utils.generate_tree import save_structure


def temp():
    from app.config import TEMP_PATH
    from app.helper import load_marshal

    data = load_marshal(TEMP_PATH.joinpath("db_with_pathes_and_accent.bin"))
    # data = load_marshal(TEMP_PATH.joinpath("db_with_pathes.bin"))
    for i, (k, v) in enumerate(data.items()):
        if i == 1:
            break
        print("\n\n", k)
        for a, b in v.items():
            print(f"{a}:\t\t\t{b}")


if __name__ == "__main__":
    pass

    # save_structure(APP_PATH)
