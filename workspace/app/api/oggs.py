from app.api.dependencies import inject_db
from app.schemas.oggs import OggAdd
from app.utils.db_manager import DBManager


@inject_db
def get_all_oggs_iter(db: DBManager, batch_size: int):
    return db.oggs.get_iter(batch_size=batch_size)


@inject_db
def get_oggs_count(db: DBManager, search: str = ""):
    return db.oggs.get_count(search or None)


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
    db.commit()


@inject_db
def delete_ogg(db: DBManager, id: int):
    """
    Удаляет запись об OGG-файле по идентификатору.

    После удаления выполняется фиксация транзакции.

    Args:
        db (DBManager): Менеджер доступа к базе данных,
            автоматически передаваемый декоратором `inject_db`.
        id (int): Идентификатор записи для удаления.

    Returns:
        None
    """
    db.oggs.delete(id=id)
    db.commit()


@inject_db
def delete_all_oggs(db: DBManager):
    """
    Удаляет все записи об OGG-файлах из базы данных.

    Args:
        db (DBManager): Менеджер доступа к базе данных,
            автоматически передаваемый декоратором `inject_db`.

    Returns:
        None
    """
    db.oggs.delete()
    db.commit()
