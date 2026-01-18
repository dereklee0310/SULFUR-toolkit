import argparse
import logging
import logging.config

import rich_argparse


class Formatter(
    rich_argparse.RawTextRichHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    pass


def setup_logger(logging_level: str) -> logging.Logger:
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        # "filters": {}
        "formatters": {
            # RichHandler do the job for us, so we don't need to incldue time & level
            "iso-8601-simple": {
                "format": "%(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            },
            "iso-8601-detailed": {
                "format": "%(asctime)s [%(levelname)s] %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            },
        },
        "handlers": {
            "stdout": {
                "level": logging_level,
                "formatter": "iso-8601-simple",
                "()": "rich.logging.RichHandler",
                "rich_tracebacks": True,
            },
            # Uncomment this if you want a rotating log file
            # "file": {
            #     "class": "logging.handlers.RotatingFileHandler",
            #     "level": "INFO",
            #     "formatter": "iso-8601-detailed",
            #     "filename": ".log",
            #     "maxBytes": 10000,
            #     "backupCount": 0,
            # },
        },
        "loggers": {"root": {"level": logging_level, "handlers": ["stdout"]}},
        # Uncomment this if you want a rotating log file
        # "loggers": {"root": {"level": "INFO", "handlers": ["stdout", "file"]}},
    }
    logging.config.dictConfig(config=logging_config)
    return logging.getLogger(__name__)


def parse_bundle_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract oil & recipe data.",
        formatter_class=Formatter,
    )
    parser.add_argument(
        "-l",
        "--log",
        dest="logging_level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level, (default: %(default)s)",
    )
    return parser.parse_args()


def parse_json_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Parse ./tmp/data.json to generate json and spreadsheet.",
        formatter_class=Formatter,
    )
    parser.add_argument(
        "-l",
        "--log",
        dest="logging_level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level, (default: %(default)s)",
    )
    parser.add_argument(
        "-d",
        "--dev",
        action="store_true",
        help="Activate developer mode to output artwork id",
    )
    return parser.parse_args()


def parse_asset_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract Sprites & Texture2D.",
        formatter_class=Formatter,
    )
    parser.add_argument(
        "-l",
        "--log",
        dest="logging_level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level, (default: %(default)s)",
    )
    type_group = parser.add_mutually_exclusive_group()
    type_group.add_argument(
        "-s",
        "--sprite",
        action="store_true",
        help="Unpack Sprite assets only",
    )
    type_group.add_argument(
        "-t",
        "--texture",
        action="store_true",
        help="Unpack Texture2D assets only",
    )
    return parser.parse_args()


def main():
    args = parse_bundle_args()
    print(args)
    logger = setup_logger(args.logging_level)
    logger.info("Hi ;)")


if __name__ == "__main__":
    main()
