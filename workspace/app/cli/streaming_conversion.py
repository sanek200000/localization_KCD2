import argparse

from app.api.tts import streaming_conversion


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--limit", type=int)
    parser.add_argument("--start-with", type=int)
    parser.add_argument("--change-dir")

    args = parser.parse_args()

    streaming_conversion(
        limit=args.limit,
        start_with=args.start_with,
        change_dir=args.change_dir,
    )


if __name__ == "__main__":
    main()
