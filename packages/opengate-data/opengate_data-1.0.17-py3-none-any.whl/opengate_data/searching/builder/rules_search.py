"""  RulesSearchBuilder """

import requests
import os
import configparser
import json
import urllib3
import re
from dotenv import load_dotenv, set_key, dotenv_values
from typing import Any
from opengate_data.searching.search import SearchBuilder
from opengate_data.utils.utils import send_request, handle_error_response, handle_exception, set_method_call, validate_type
from requests import Response


class RulesSearchBuilder(SearchBuilder):
    """ Class rules builder"""

    def __init__(self, opengate_client):
        super().__init__()
        self.client = opengate_client
        self.headers = self.client.headers
        self.url: str | None = None
        self.body_data: dict = {}
        self.builder: bool = False
        self.method_calls: list = []

    @set_method_call
    def build(self) -> 'RulesSearchBuilder':
        """
        Finalizes the construction of the datapoints search configuration.

        This method prepares the builder to execute the collection by ensuring all necessary configurations are set and validates the overall integrity of the build. It should be called before executing the collection to ensure that the configuration is complete and valid.

        Returns:
            DataPointsSearchBuilder: Returns itself to allow for method chaining.

        Raises:
            ValueError: If required configurations are missing or if incompatible methods are used together.
        """
        self.builder = True
        self._validate_builds()

        if self.method_calls.count('build_execute') > 0:
            raise Exception("You cannot use build() together with build_execute()")

        return self

    def build_execute(self):
        """
        Executes the datapoints search immediately after building the configuration.

        This method is a shortcut that combines building and executing in a single step.

        Returns:
            dict: A dictionary containing the execution response which includes the status code and potentially other metadata about the execution.

        Raises:
            ValueError: If `build` has already been called on this builder instance.
        """
        if self.method_calls.count('build') > 0:
            raise ValueError("You cannot use build_execute() together with build()")

        if self.method_calls.count('execute') > 0:
            raise ValueError("You cannot use build_execute() together with execute()")

        return self.execute()

    def execute(self):
        """
        Executes the operations search based on the built configuration.

        Returns:
            dict: The response data.

        Raises:
            Exception: If the build() method was not called before execute().
        """
        if not self.builder or self.method_calls[-2] != 'build':
            raise Exception(
                "The build() function must be called and must be the last method invoked before execute")

        url = f'{self.client.url}/north/v80/rules/search'
        return self.rules_dict_request(self.client.headers, url, self.body_data)

    @staticmethod
    def rules_dict_request(headers: dict, url: str, body_data: dict) -> Any:
        all_results = []
        limit = body_data.get("limit", {})
        start = limit.get("start", 1)
        size = limit.get("size", 1000)
        has_limit = "limit" in body_data

        while True:
            body_data.setdefault("limit", {}).update({"start": start, "size": size})
            try:
                response = send_request(method='post', headers=headers, url=url, json_payload=body_data)

                if response.status_code == 204:
                    if all_results:
                        break
                    return {'status_code': response.status_code}

                if response.status_code != 200 and response.status_code != 204:
                    return handle_error_response(response)

                data = response.json()

                if not data.get('rules'):
                    break

                all_results.extend(data['rules'])

                if has_limit:
                    break

                start += 1

            except Exception as e:
                return handle_exception(e)

        return all_results
