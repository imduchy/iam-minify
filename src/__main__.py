import json
import logging
import sys

from src.config import ArgumentParser, Config
from src.actions import IAMActions
from src.truncate import merge_overlaps, truncate

LOGGER = logging.getLogger("iam-minify")


def main() -> int:
    cli_args = ArgumentParser().parse_args()

    config = Config(cli_args)

    try:
        # Get the path to the file containing IAM actions
        file_path = config.file_path

        with open(file_path, "r", encoding="utf-8") as f:
            provided_actions = json.load(f)

    except FileNotFoundError:
        LOGGER.error(
            "The file doesn't exist. Provide a valid path to a JSON file containing a list of "
            "valid IAM actions."
        )
        return 1

    # Fetch the list of all IAM actions
    all_actions = IAMActions()

    truncated_permissions = truncate(provided_actions, all_actions.as_list)
    optimized_list = merge_overlaps(truncated_permissions, all_actions.as_list)

    LOGGER.info(json.dumps(optimized_list, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
