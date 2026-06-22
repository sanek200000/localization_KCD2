import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))


from app.models.subs import SubsOrm
from app.api.subs import delete_all_subs, get_null_accent, get_subs_by_filter
from app.accent import fill_subs
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

    # data = get_subs_by_filter(SubsOrm.ru_accent.is_(None), SubsOrm.ru_sub.is_not(None))
    data = get_null_accent()
    print(len(data))
    # result = DataMapper().map_to_domain_entity(data[0]).model_dump()

    for i, item in enumerate(data):
        if i == 4:
            break
        print(f"{item.id = }\n{item.ru_sub = }\n{item.ru_accent = }\n\n")

    # fill_subs()
    # delete_all_subs()
    # temp()
    # delete_all_oggs()
    # list_all_oggs()
