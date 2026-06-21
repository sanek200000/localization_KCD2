import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))


from app.api.oggs import delete_all_oggs
from app.make_db import list_all_oggs


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

    temp()

    # delete_all_oggs()
    # list_all_oggs()
