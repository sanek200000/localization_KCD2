from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import SS


ENGINE = create_engine(
    url=SS.DB_URL,
    # echo=True,
    connect_args={"check_same_thread": False},
)
SESSION_MAKER = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """
    Базовый декларативный класс для всех ORM-моделей приложения.

    Наследование от данного класса позволяет SQLAlchemy автоматически
    регистрировать модели и связывать их с общей метаинформацией
    (`metadata`), используемой для создания, изменения и управления
    структурой базы данных.

    Notes:
        - Все ORM-модели приложения должны наследоваться от `Base`.
        - Метаданные доступны через атрибут `Base.metadata`.
        - Используется совместно с объектами `ENGINE` и
          `SESSION_MAKER` для работы с базой данных.
    """

    pass


def check_db_connect():
    try:
        print(f"{ENGINE.url}")
        with ENGINE.connect() as conn:
            result = conn.execute(
                text("SELECT name FROM sqlite_master WHERE type='table';")
            )
            print(f"\n{result.fetchall() = }\n")
        print("Подключение успешно")
    except Exception as e:
        print(f"Ошибка подключения: {e}")


if __name__ == "__main__":
    pass
