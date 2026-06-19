import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.make_db import list_all_oggs


if __name__ == "__main__":
    pass

    list_all_oggs()
