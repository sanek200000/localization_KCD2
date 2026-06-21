from app.db import SESSION_MAKER
from app.repositories.oggs import OggsRepository
from app.repositories.subs import SubsRepository


class DBManager:
    """
    Менеджер работы с базой данных.

    Инкапсулирует создание и управление SQLAlchemy-сессией,
    предоставляет доступ к репозиториям приложения и обеспечивает
    корректное закрытие соединения через протокол контекстного
    менеджера.

    Attributes:
        session_factory: Фабрика сессий SQLAlchemy, используемая
            для создания новых соединений с базой данных.
        session (Session): Активная сессия базы данных.
        oggs (OggsRepository): Репозиторий для работы с OGG-файлами.
    """

    def __init__(self, session_factory: SESSION_MAKER):
        """
        Инициализирует менеджер базы данных.

        Args:
            session_factory: Фабрика сессий SQLAlchemy
                (`sessionmaker`).
        """
        self.session_factory = session_factory

    def __enter__(self):
        """
        Создает новую сессию базы данных и инициализирует репозитории.

        Returns:
            DBManager: Текущий экземпляр менеджера с активной сессией.
        """
        self.session = self.session_factory()

        self.oggs = OggsRepository(self.session)
        self.subs = SubsRepository(self.session)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Завершает работу сессии при выходе из контекстного менеджера.

        При возникновении исключения выполняется откат транзакции,
        после чего сессия закрывается.

        Args:
            exc_type: Тип возникшего исключения.
            exc_val: Экземпляр исключения.
            exc_tb: Объект traceback.
        """
        if exc_type:
            self.session.rollback()

        self.session.close()

    def commit(self):
        """Фиксирует текущую транзакцию в базе данных."""
        self.session.commit()

    def rollback(self):
        """Выполняет откат текущей транзакции."""
        self.session.rollback()
