import json
import logging

LOGGER = logging.getLogger("iam-minify")


def load_policy_document(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            policy_document = json.load(f)

        return policy_document
    except FileNotFoundError as err:
        LOGGER.error(
            "A file under path %s doesn't exist. Provide a path to a valid IAM policy "
            "document in the JSON format.",
            path,
        )
        raise err

    except json.JSONDecodeError as err:
        LOGGER.error("The file must contain a valid IAM policy in JSON format.")
        raise err
