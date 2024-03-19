import json
import sys
import argparse

from src.actions import IAMActions
from src.truncate import merge_overlaps, truncate

arg_parser = argparse.ArgumentParser("iamtrunc")
arg_parser.add_argument(
    "-f",
    "--file-path",
    help="Path to a JSON file containing a list of IAM actions",
    required=True,
)

if __name__ == "__main__":
    args = arg_parser.parse_args()

    try:
        # Get the path to the file containing IAM actions
        file_path = args.file_path

        with open(file_path, "r", encoding="utf-8") as f:
            provided_actions = json.load(f)

    except FileNotFoundError as err:
        print(
            "Error: The file doesn't exist. Provide a valid path to a JSON file containing a list "
            "of valid IAM actions."
        )
        sys.exit(1)

    # Fetch the list of all IAM actions
    all_actions = IAMActions()

    truncated_permissions = truncate(provided_actions, all_actions.as_list)
    optimized_list = merge_overlaps(truncated_permissions, all_actions.as_list)

    print(json.dumps(optimized_list, indent=2))
