from config import logger

from app.api.tts import convert_audio_with_remote_session
from app.services.conveyor import conveyor_models


if __name__ == "__main__":
    logger.info("----------------------START NEW SESSION----------------------")

    # convert_audio_with_remote_session(limit=10)
    conveyor_models()

    logger.info("----------------------END SESSION----------------------")
