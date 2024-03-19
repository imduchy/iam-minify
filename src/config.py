import argparse
import logging
from argparse import Namespace

LOGGER = logging.getLogger("iam-minify")


def configure_logging(debug_logging: bool):
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    if debug_logging:
        LOGGER.setLevel(logging.DEBUG)
    else:
        LOGGER.setLevel(logging.INFO)

    log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(log_formatter)

    LOGGER.addHandler(handler)


class ArgumentParser:
    def __init__(self) -> None:
        self._arg_parser = argparse.ArgumentParser("iam-minify")
        self._add_arguments()

    def parse_args(self) -> Namespace:
        return self._arg_parser.parse_args()

    def _add_arguments(self):
        self._arg_parser.add_argument(
            "-f",
            "--file-path",
            help="Path to a JSON file containing a list of IAM actions",
            required=True,
        )

        self._arg_parser.add_argument(
            "-d",
            "--debug",
            help="Enable debug logging",
            action="store_true",
            default=False,
            required=False,
        )


class Config:
    def __init__(self, cli_args: Namespace) -> None:
        self.file_path = cli_args.file_path

        configure_logging(cli_args.debug)
