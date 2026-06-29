from pathlib import Path

from app.config import TEMP_PATH

IGNORE_LIST = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
    "project_structure.txt",  # Игнорируем сам файл отчета
}


def build_tree(dir_path: Path, prefix: str = "") -> list:
    tree_lines = []

    try:
        items = sorted(
            [x for x in dir_path.iterdir() if x.name not in IGNORE_LIST],
            key=lambda x: (not x.is_dir(), x.name.lower()),
        )
    except PermissionError:
        return [f"{prefix}└── [Ошибка доступа]"]

    count = len(items)
    for index, item in enumerate(items):
        is_last = index == count - 1
        connector = "└── " if is_last else "├── "

        suffix = "/" if item.is_dir() else ""
        tree_lines.append(f"{prefix}{connector}{item.name}{suffix}")

        if item.is_dir():
            next_prefix = prefix + ("    " if is_last else "│   ")
            tree_lines.extend(build_tree(item, next_prefix))

    return tree_lines


def save_structure(root_dir: Path):

    tree = [f"{root_dir.name}/"] + build_tree(root_dir)

    output_file = TEMP_PATH.joinpath("project_structure.txt")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(tree))

    print(f"Структура успешно сохранена в файл: {output_file.name}")
