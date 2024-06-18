import urllib.request
import json
import logging


class AzureDeployedModel:
    """Wrapper class for Azure deployed model."""

    def __init__(
        self,
        endpoint_url: str,
        api_key: str,
    ) -> None:
        self.endpoint_url = endpoint_url
        self.api_key = api_key

    def _convert_bytes_to_list(self, val: bytes) -> list:
        """Convert the bytes to list."""
        try:
            # Attempt to decode the input string as JSON
            result_dict = json.loads(val)

            if isinstance(result_dict, list):
                # Check if the parsed JSON is a list
                if result_dict:
                    return result_dict[0]
                else:
                    return []
            else:
                return []
        except json.JSONDecodeError:
            # Handle JSON decoding error
            return []


    def predict(self, input_blob: dict) -> list:
        """Invoke the deployed model and return the result."""
        body = str.encode(json.dumps(input_blob))

        if not self.api_key:
            raise Exception("A key should be provided to invoke the endpoint")

        headers = {
            "Content-Type": "application/json",
            "Authorization": ("Bearer " + self.api_key),
            "azureml-model-deployment": "high-level-categorize-queries-2",
        }

        req = urllib.request.Request(self.endpoint_url, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read()
            return self._convert_bytes_to_list(result)

        except urllib.error.HTTPError as error:
            logging.info("The request failed with status code: " + str(error.code))

            logging.info(error.info())
            logging.info(error.read().decode("utf8", "ignore"))
