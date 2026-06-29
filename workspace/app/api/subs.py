from app.api.dependencies import inject_db
from app.schemas.subs import SubAddDTO, SubPatchDTO
from app.utils.db_manager import DBManager


@inject_db
def get_all_subs_iter(db: DBManager, batch_size: int):
    return db.subs.iter_subs_with_oggs(batch_size=batch_size)


@inject_db
def get_subs_by_filter(db: DBManager, *args, **kwargs):
    """
    Получает список субтитров по заданным фильтрам.

    Args:
        db (DBManager): Менеджер базы данных.
        *args: SQLAlchemy-выражения фильтрации.
        **kwargs: Именованные фильтры по полям модели.

    Returns:
        list: Список субтитров, удовлетворяющих условиям фильтрации.
    """
    return db.subs.get_filtred(*args, **kwargs)


@inject_db
def get_null_accent(db: DBManager):
    """
    Получает субтитры без расставленных ударений.

    Возвращает записи, у которых поле `ru_accent` не заполнено,
    но присутствует русский текст (`ru_sub`).

    Args:
        db (DBManager): Менеджер базы данных.

    Returns:
        list: Список субтитров без `ru_accent`.
    """
    return db.subs.get_null_accent()


@inject_db
def get_sub(db: DBManager, sub_id: int):
    """
    Получает один субтитр по его идентификатору.

    Args:
        db (DBManager): Менеджер базы данных.
        sub_id (int): Идентификатор субтитра.

    Returns:
        SubsOrm | None: Найденный объект субтитра или None.
    """
    return db.subs.get_one(id=sub_id)


@inject_db
def add_sub(db: DBManager, data: SubAddDTO):
    """
    Создает новый субтитр в базе данных.

    Args:
        db (DBManager): Менеджер базы данных.
        data (SubAddDTO): Данные нового субтитра.

    Returns:
        None
    """
    result = db.subs.add(data)
    print(f"{result = }")
    db.commit()


@inject_db
def patch_sub(db: DBManager, sub_id: int, data: SubPatchDTO):
    """
    Частично обновляет субтитр по идентификатору.

    Args:
        db (DBManager): Менеджер базы данных.
        sub_id (int): Идентификатор субтитра.
        data (SubPatchDTO): Частичные данные для обновления.

    Returns:
        None
    """
    db.subs.edit(data=data, exclude_unset=True, id=sub_id)
    db.commit()


@inject_db
def delete_sub(db: DBManager, sub_id: int):
    """
    Удаляет субтитр по идентификатору.

    Args:
        db (DBManager): Менеджер базы данных.
        sub_id (int): Идентификатор записи.

    Returns:
        None
    """
    db.subs.delete(sub_id=id)
    db.commit()


@inject_db
def delete_all_subs(db: DBManager):
    """
    Удаляет все субтитры из базы данных.

    Returns:
        None

    Warning:
        Операция необратима и удаляет все данные без фильтрации.
    """
    db.subs.delete()
    db.commit()
