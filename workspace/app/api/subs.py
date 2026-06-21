from app.api.dependencies import inject_db
from app.schemas.subs import SubAdd
from app.utils.db_manager import DBManager


@inject_db
def get_subs(db: DBManager):
    return db.subs.get_all()


@inject_db
def add_sub(db: DBManager, data: SubAdd):
    result = db.subs.add(data)
    print(f"{result = }")
    # db.commit()


@inject_db
def delete_sub(db: DBManager, id: int):
    db.subs.delete(id=id)
    db.commit()


@inject_db
def delete_all_subs(db: DBManager):
    all_subs = db.subs.get_all()
    for sub in all_subs:
        delete_sub(id=sub.id)
