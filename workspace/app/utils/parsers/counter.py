from pathlib import Path

from loguru import logger


def get_files_count_by_path(path: Path, mask: str):
    logger.info(f"Searching in: {path} with mask: {mask}")

    # count = 0
    #
    # for file in path.rglob(mask):
    #     if file.is_file():
    #         count += 1
    #
    #         if count % 1000 == 0:
    #             yield count
    #
    # yield count

    count = sum(1 for item in path.rglob(mask) if item.is_file())
    logger.info(count)

    return count
