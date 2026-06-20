from app.api.dependencies import inject_db
from app.schemas.oggs import OggAdd
from app.utils.db_manager import DBManager


@inject_db
def add_ogg(db: DBManager, data: OggAdd):
    """
    Добавляет запись об OGG-файле в базу данных.

    Функция использует репозиторий `oggs` объекта `DBManager`
    для создания новой записи на основе данных, переданных
    в модели `OggAdd`.

    Args:
        db (DBManager): Менеджер доступа к базе данных,
            автоматически передаваемый декоратором `inject_db`.
        data (OggAdd): Данные OGG-файла для сохранения.

    Returns:
        None
    """

    result = db.oggs.add(data)
    print(f"{result = }")
    # db.commit()


@inject_db
def delete_ogg(db: DBManager, id: int):
    db.oggs.delete(id=id)
    db.commit()


@inject_db
def delete_all_oggs(db: DBManager):
    all_oggs = db.oggs.get_all()
    for ogg in all_oggs:
        delete_ogg(id=ogg.id)
