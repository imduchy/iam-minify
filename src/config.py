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

    log_formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(log_formatter)

    LOGGER.addHandler(handler)


class ArgumentParser:
    def __init__(self) -> None:
        self._arg_parser = argparse.ArgumentParser(
            prog="iam-minify",
            description=(
                "Optimize long AWS IAM policies by strategically using wildcards, reducing the "
                "number of characters, and maintaining the intended scope of permissions."
            ),
            epilog="Find more information at https://github.com/imduchy/iam-minify",
        )
        self._add_arguments()

    def parse_args(self) -> Namespace:
        return self._arg_parser.parse_args()

    def _add_arguments(self):
        self._arg_parser.add_argument(
            "policy",
            help="the IAM policy document that should be minified (only supports JSON files)",
            type=str,
        )

        self._arg_parser.add_argument(
            "-d",
            "--debug",
            help="enable debug logging",
            action="store_true",
            default=False,
            required=False,
        )


class Config:
    def __init__(self, cli_args: Namespace) -> None:
        self.policy_document_path = cli_args.policy

        configure_logging(cli_args.debug)
