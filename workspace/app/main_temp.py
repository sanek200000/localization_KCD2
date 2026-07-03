import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.utils.generate_tree import save_structure

if __name__ == "__main__":
    save_structure()
