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
            policy_document = json.load(f)

    except FileNotFoundError:
        LOGGER.error(
            "The file doesn't exist. Provide a valid path to a JSON file containing a list of "
            "valid IAM actions."
        )
        return 1

    # Fetch the list of all IAM actions
    all_actions = IAMActions()

    for statement in policy_document["Statement"]:
        actions = statement["Action"]

        truncated = truncate(actions, all_actions.as_list)
        merged = merge_overlaps(truncated, all_actions.as_list)

        # Overwrite the original list of actions within the statement
        statement["Action"] = merged

    LOGGER.info(json.dumps(policy_document, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
