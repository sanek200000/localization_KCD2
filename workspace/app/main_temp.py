import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))

from app.api.tts import get_models, load_model
from app.utils.generate_tree import save_structure

if __name__ == "__main__":
    # save_structure()

    models = get_models()
    print(models)

    for id, value in models.items():
        print(value.get("name"))
