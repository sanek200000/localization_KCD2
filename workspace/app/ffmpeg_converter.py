#!/usr/bin/env python3

import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from helper import load_marshal, append_txt

DB_WITH_FILES_PATHES = Path("./temp/db_with_pathes.bin")
KEYS_WITHOUT_OGG = Path("./temp/keys_without_oggs.txt")


def convert_ogg_to_wav_onethread(data: dict):
    DEBUG = 0

    for i, (key, value) in enumerate(data.items()):
        if DEBUG and i == 30:
            break
        if key == "nothing":
            convert_ogg_to_wav_onethread(data.get("nothing"))
            # continue

        print(key, value, sep="\n", end="\n\n")
        input_ogg = Path(value.get("ogg_en_path")).resolve()
        output_wav = Path(value.get("wav_en_path")).resolve()
        if not output_wav.exists():
            output_wav.parent.mkdir(parents=True, exist_ok=True)
            command = (
                f"ffmpeg -i {input_ogg} -ac 1 -ar 24000 -c:a pcm_s16le {output_wav}",
            )
            subprocess.run(command, shell=True, check=True)


def process_item(item: dict):
    key, value = item

    # input_ogg = Path(value["ogg_en_path"]).resolve()
    # output_wav = Path(value["wav_en_path"]).resolve()
    try:
        input_ogg = Path(value.get("ogg_en_path")).resolve()
        output_wav = Path(value.get("wav_en_path")).resolve()
    except:
        append_txt(KEYS_WITHOUT_OGG, key)
        return

    if output_wav.exists():
        return

    output_wav.parent.mkdir(parents=True, exist_ok=True)
    command = f"ffmpeg -i {input_ogg} -ac 1 -ar 24000 -c:a pcm_s16le {output_wav}"
    subprocess.run(command, shell=True, check=True)

    # subprocess.run(
    #     [
    #         "ffmpeg",
    #         "-i",
    #         str(input_ogg),
    #         "-ac",
    #         "1",
    #         "-ar",
    #         "24000",
    #         "-c:a",
    #         "pcm_s16le",
    #         str(output_wav),
    #     ],
    #     check=True,
    # )


def iter_items(data: dict):
    for key, value in data.items():
        if key == "nothing":
            yield from iter_items(value)
        else:
            yield key, value


def convert_ogg_to_wav(data: dict):
    with ThreadPoolExecutor(max_workers=20) as executor:
        list(executor.map(process_item, iter_items(data)))


if __name__ == "__main__":
    pass

    data = load_marshal(DB_WITH_FILES_PATHES)
    convert_ogg_to_wav(data)
