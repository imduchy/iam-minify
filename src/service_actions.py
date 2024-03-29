import json
import logging

import requests

LOGGER = logging.getLogger("iam-minify")
IAM_ACTIONS_URL = "https://awspolicygen.s3.amazonaws.com/js/policies.js"


class AWSServiceActionsNotFetchedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class AWSServiceActionsNotParsedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class AWSServiceActions:
    def __init__(self) -> None:
        self._iam_actions = {}
        self._fetch_and_parse()

    @property
    def as_dict(self):
        return self._iam_actions

    @property
    def as_list(self):
        return [action for actions in self._iam_actions.values() for action in actions]

    def _fetch_and_parse(self) -> str:
        try:
            LOGGER.debug("Fetching AWS service actions from %s", IAM_ACTIONS_URL)
            response = requests.get(IAM_ACTIONS_URL, timeout=5)

            LOGGER.debug("Status code: %d", response.status_code)
        except Exception as err:
            raise AWSServiceActionsNotFetchedError(
                f"Couldn't fetch AWS service actions data from the URL {IAM_ACTIONS_URL}"
            ) from err

        try:
            LOGGER.debug("Parsing the response from the endpoint")
            self._parse_data(response.text)
        except AWSServiceActionsNotParsedError as err:
            raise AWSServiceActionsNotParsedError(
                f"Couldn't parse AWS service actions data from the URL {IAM_ACTIONS_URL}"
            ) from err

    def _parse_data(self, resp_string: str):
        resp_string = resp_string.replace("app.PolicyEditorConfig=", "")
        resp_json = json.loads(resp_string)

        service_map: dict = resp_json["serviceMap"]

        for service in service_map.values():
            prefix: str = service["StringPrefix"]
            actions: list[str] = service["Actions"]

            self._iam_actions[prefix] = [f"{prefix}:{action}" for action in actions]
