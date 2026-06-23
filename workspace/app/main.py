import sys
from pathlib import Path

from tqdm import tqdm


sys.path.append(str(Path(__file__).parent.parent))


from app.schemas.subs import SubPatchDTO
from app.models.subs import SubsOrm
from app.api.subs import (
    get_null_accent,
    get_sub,
    patch_sub,
)
from app.accent import convert_ru_sub
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

    data = get_null_accent()
    print(len(data))
    for i, item in enumerate(tqdm(data, desc="Add RU accent: ")):
        # if i == 2:
        #     break

        res = convert_ru_sub(item.ru_sub)
        # print(f"{res = }")
        patch_sub(sub_id=item.id, data=SubPatchDTO(ru_accent=res))

        # r = get_sub(sub_id=item.id)
        # print(r.id, r.ru_sub, r.ru_accent, sep="\n\t")

        # print(f"{item.oggs = }\n{item.ru_sub = }\n{item.ru_accent = }\n\n")

    # fill_subs()
    # delete_all_subs()
    # temp()
    # delete_all_oggs()
    # list_all_oggs()
