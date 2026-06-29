from functools import wraps

from app.clients.tts import TTSClient
from app.db import SESSION_MAKER
from app.utils.db_manager import DBManager


def inject_db(func):
    """
    Декоратор для автоматической передачи объекта DBManager
    в вызываемую функцию.

    При каждом вызове декорируемой функции создается новый экземпляр
    `DBManager` на основе `SESSION_MAKER`, который передается первым
    позиционным аргументом. Управление жизненным циклом сессии
    осуществляется через контекстный менеджер.

    Args:
        func (Callable): Функция, принимающая объект `DBManager`
            первым аргументом.

    Returns:
        Callable: Обернутая функция с автоматически внедренным
        объектом `DBManager`.

    Notes:
        Декорируемая функция должна иметь следующую сигнатуру:

        >>> @inject_db
        >>> def my_func(db, *args, **kwargs):
        >>>     ...

        где `db` — экземпляр `DBManager`.

    Side Effects:
        - Создает новую сессию базы данных при каждом вызове функции.
        - Автоматически закрывает сессию после завершения работы.
        - Делегирует управление транзакциями объекту `DBManager`.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        with DBManager(SESSION_MAKER) as db:
            return func(db, *args, **kwargs)

    return wrapper


def inject_tts(func):
    """
    Декоратор для автоматического управления жизненным циклом TTS-клиента.

    Создаёт экземпляр `TTSClient` в контекстном менеджере и передаёт его
    в декорируемую функцию как первый позиционный аргумент.

    Обеспечивает корректное открытие и закрытие ресурсов TTS-клиента
    без необходимости явного управления соединением в бизнес-логике.

    Args:
        func (Callable): Функция, принимающая `tts_client` как первый
            аргумент.

    Returns:
        Callable: Обёрнутая функция с внедрённым TTS-клиентом.

    Notes:
        - Использует контекстный менеджер `TTSClient()`.
        - Гарантирует освобождение ресурсов после выполнения функции.
        - Пробрасывает все исключения, возникающие внутри функции.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        with TTSClient() as tts_client:
            return func(tts_client, *args, **kwargs)

    return wrapper
