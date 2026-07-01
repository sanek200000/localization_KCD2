import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))

from app.api.tts import convert_audio_with_session
from app.config import APP_PATH
from app.utils.generate_tree import save_structure


if __name__ == "__main__":
    pass

    convert_audio_with_session(limit=100)
    # save_structure(APP_PATH)
