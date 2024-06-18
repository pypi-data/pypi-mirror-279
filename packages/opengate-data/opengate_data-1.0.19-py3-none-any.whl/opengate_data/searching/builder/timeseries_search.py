"""  timeseriesBuilder """

import requests
import pandas as pd
from typing import Any
from opengate_data.searching.search import SearchBuilder
from opengate_data.utils.utils import send_request, handle_error_response, handle_exception, set_method_call, \
    validate_type

class TimeseriesSearchBuilder:
    """ Dataset Builder """

    def __init__(self, opengate_client):
        self.client = opengate_client
        self.headers = self.client.headers
        self.organization_name: str | None = None
        self.identifier: str | None = None
        self.body_data: dict[str, Any] = {}
        self.format_data: str = 'dict'
        self.utc: str | None = None
        self.builder: bool = False
        self.method_calls = []

    @set_method_call
    def with_organization_name(self, organization_name: str) -> 'TimeseriesSearchBuilder':
        """
        Set organization name

        Returns:
            TimeseriesSearchBuilder: Returns itself to allow for method chaining.
        """
        validate_type(organization_name, str, "Organization")
        self.organization_name = organization_name
        return self

    @set_method_call
    def with_identifier(self, identifier: str) -> 'TimeseriesSearchBuilder':
        """
        Set identifier

        Returns:
            TimeseriesSearchBuilder: Returns itself to allow for method chaining.
        """
        validate_type(identifier, str, "Identifier")
        self.identifier = identifier
        return self

    def with_utc(self) -> 'TimeseriesSearchBuilder':
        """
        Set UTC

        Returns:
            TimeseriesSearchBuilder: Returns itself to allow for method chaining.
        """
        self.utc = True
        return self

    @set_method_call
    def with_format(self, format_data: str) -> 'TimeseriesSearchBuilder':
        """
        Formats the flat entities data based on the specified format ('csv', 'dict', or 'pandas').

        Args:
            format_data (str): The format to use for the data.

        Returns:
            SearchBuilder: Returns itself to allow for method chaining.
        """
        validate_type(format_data, str, "Format data")
        self.format_data = format_data
        if self.format_data == 'csv':
            self.headers['Accept'] = 'text/plain'
        else:
            self.headers['Accept'] = 'application/json'
        return self

    @set_method_call
    def build(self) -> 'TimeseriesSearchBuilder':
        """
        Finalizes the construction of the operations search configuration.

        This method prepares the builder to execute the collection by ensuring all necessary configurations are set and validates the overall integrity of the build. It should be called before executing the collection to ensure that the configuration is complete and valid.

        The build process involves checking that mandatory fields such as the device identifier are set. It also ensures that method calls that are incompatible with each other (like `build` and `build_execute`) are not both used.

        Example:
            builder.build()

        Returns:
            OperationsSearchBuilder: Returns itself to allow for method chaining, enabling further actions like `execute`.

        Raises:
            ValueError: If required configurations are missing or if incompatible methods are used together.

        Note:
            This method should be used as a final step before `execute` to prepare the operations search configuration. It does not modify the state but ensures that the builder's state is ready for execution.
        """
        self.builder = True
        self._validate_builds()

        if self.method_calls.count('build_execute') > 0:
            raise Exception("You cannot use build() together with build_execute()")

        return self

    @set_method_call
    def build_execute(self):
        """
        Executes the data sets search immediately after building the configuration.

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

        self._validate_builds()
        return self.execute()

    def _validate_builds(self):
        if self.method_calls.count('with_format') > 1:
            raise Exception("You cannot use more than one with_format() method")

        if "with_organization_name" not in self.method_calls and "with_identifier" not in self.method_calls:
            raise Exception("It is mandatory to use the with_organization_name() and with_identifier() methods")

        return self

    def execute(self):
        url = f'{self.client.url}/north/v80/timeseries/provision/organizations/{self.organization_name}/{self.identifier}/data?utc={self.utc}'
        return self._dict_pandas_request(self.client.headers, url, self.body_data)

    def _dict_pandas_request(self, headers: dict, url: str, body_data: dict) -> Any:
        all_results = []
        data = None
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

                if not data.get('data'):
                    break

                all_results.extend(data['data'])

                if has_limit:
                    break

                start += 1

            except Exception as e:
                return handle_exception(e)

        return self._format_results(all_results, data['columns'])

    def _format_results(self, all_results: list, columns: list) -> Any:
        if self.format_data in ['dict', None]:
            dict_data = []
            for fila in all_results:
                fila_dict = {columns[i]: fila[i] for i in range(len(columns))}
                dict_data.append(fila_dict)
            return dict_data

        if self.format_data == 'pandas':
            return pd.DataFrame(all_results, columns=columns)

        raise ValueError(f"Unsupported format: {self.format_data}")
