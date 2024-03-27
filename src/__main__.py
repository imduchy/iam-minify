"""
Optimize long AWS IAM policies by strategically using wildcards, reducing the number of characters,
and maintaining the intended scope of permissions.
"""

import json
import logging
import sys

from src.service_actions import AWSServiceActions
from src.config import ArgumentParser, Config
from src.file_helpers import load_policy_document
from src.optimize import merge_overlaps, truncate

LOGGER = logging.getLogger("iam-minify")


def main() -> int:
    cli_args = ArgumentParser().parse_args()
    config = Config(cli_args)

    # Load JSON file containing IAM policy document
    policy_document = load_policy_document(config.policy_document_path)

    # Fetch actions for all available AWS services
    service_actions = AWSServiceActions()

    # Process each of the policy statements separately
    for statement in policy_document["Statement"]:
        policy_actions = statement["Action"]

        truncated = truncate(policy_actions, service_actions.as_list)
        merged = merge_overlaps(truncated, service_actions.as_list)

        # Overwrite the original list of actions within the statement
        statement["Action"] = merged

    LOGGER.info(json.dumps(policy_document, indent=2))

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())

    # pylint: disable=W0718
    except Exception as err:
        LOGGER.error(err)
        sys.exit(1)
