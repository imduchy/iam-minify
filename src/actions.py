import json
import logging

import requests

LOGGER = logging.getLogger("iam-minify")
FILE_URL = "https://awspolicygen.s3.amazonaws.com/js/policies.js"


class IAMActions:
    def __init__(self) -> None:
        self._iam_actions = dict()
        self._fetch_and_parse()

    @property
    def as_dict(self):
        return self._iam_actions

    @property
    def as_list(self):
        return [action for actions in self._iam_actions.values() for action in actions]

    def _fetch_and_parse(self) -> str:
        try:
            LOGGER.debug("Fetching IAM actions from %s", FILE_URL)
            response = requests.get(FILE_URL, timeout=5)

            return self._parse_data(response.text)
        except Exception as err:
            raise err

    def _parse_data(self, resp_string: str):
        resp_string = resp_string.replace("app.PolicyEditorConfig=", "")
        resp_json = json.loads(resp_string)

        service_map: dict = resp_json["serviceMap"]

        for service in service_map.values():
            prefix = service["StringPrefix"]
            actions = service["Actions"]

            self._iam_actions[prefix] = [f"{prefix}:{action}" for action in actions]
