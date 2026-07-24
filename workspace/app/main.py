from config import logger

# from app.api.tts import streaming_conversion
# from app.services.conveyor import conveyor_models

# from app.gui.server import run

from nicegui import ui
import app.gui.routers

logger.info("----------------------START NEW SESSION----------------------")
ui.run(
    dark=True,
    reload=True,
    favicon="🎙️",
    title="KCD2 localization",
)

if __name__ == "__main__":
    pass
    logger.info("----------------------END SESSION----------------------")

    # convert_audio_with_remote_session(limit=10)
    # conveyor_models()
    # run()
