import sys
from pathlib import Path
from pydantic_settings import BaseSettings
from loguru import logger

sys.path.append(str(Path(__file__).parent.parent))

BASE_DIR = Path(__file__).resolve().parent.parent

APP_PATH = BASE_DIR.joinpath("app/")
LOCALIZATION_PATH = BASE_DIR.joinpath("localization/")
TEMP_PATH = BASE_DIR.joinpath("temp/")
GAME_FOLDER = BASE_DIR.joinpath("kcd2/")

logger.remove()
logger.add(
    APP_PATH.joinpath("logs/kcd2_localization_client.log"),
    rotation="100 minute",
    retention=2,
)


class Settings(BaseSettings):
    DB_PATH: str = str("/db/kcd2.db")
    tts_server_url: str
    tts_timeout: int = 300

    @property
    def DB_URL(self):
        return f"sqlite:///{self.DB_PATH}"


SS = Settings()

if __name__ == "__main__":
    print(f"{SS.DB_URL = }")

    [
        print(f"{key}: {value}")
        for key, value in globals().items()
        if not key.startswith("__")
    ]
