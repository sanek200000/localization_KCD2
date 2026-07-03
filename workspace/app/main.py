from config import logger
from app.api.tts import convert_audio_with_remote_session


if __name__ == "__main__":
    logger.info("----------------------START NEW SESSION----------------------")

    convert_audio_with_remote_session(limit=1)

    logger.info("----------------------END SESSION----------------------")
