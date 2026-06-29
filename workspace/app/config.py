from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

APP_PATH = BASE_DIR.joinpath("app/")
LOCALIZATION_PATH = BASE_DIR.joinpath("localization/")
TEMP_PATH = BASE_DIR.joinpath("temp/")
GAME_FOLDER = BASE_DIR.joinpath("kcd2/")


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
