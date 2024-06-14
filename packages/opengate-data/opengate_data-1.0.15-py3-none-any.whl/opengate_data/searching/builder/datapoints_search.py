""" DatapointsSearchBuilder """

import requests
import json
import pandas as pd
from io import StringIO
from typing import Any, Dict
from flatten_dict import flatten
from opengate_data.searching.search import SearchBuilder
from opengate_data.utils.utils import send_request, handle_error_response, handle_exception, set_method_call, validate_type
from opengate_data.searching.search_base import SearchBuilderBase
from urllib.parse import urlencode


class DataPointsSearchBuilder(SearchBuilderBase, SearchBuilder):
    """Builder for datapoints search"""

    def __init__(self, opengate_client):
        super().__init__()
        self.client = opengate_client
        self.headers = self.client.headers
        self.transpose: bool = False
        self.mapping: dict[str, dict[str, str]] | None = None
        self.builder: bool = False
        self.url: str | None = None

    @set_method_call
    def with_transpose(self) -> 'DataPointsSearchBuilder':
        """
        Enable transposing of the data.

        This method sets the transpose flag to True, indicating that the data should be transposed during processing.
        Transposing the data means converting rows into columns and vice versa, which can be useful for certain types
        of data analysis and visualization.

        Returns:
            DataPointsSearchBuilder: Returns itself to allow for method chaining.
        """
        self.transpose = True
        return self

    @set_method_call
    def with_mapped_transpose(self, mapping: dict[str, dict[str, str]]) -> 'DataPointsSearchBuilder':
        """
        Enable mapped transposing of the data.

        This method sets the mapping for transposing the data, allowing for specific columns to be mapped to new values
        based on JSON path expressions. This is useful when you need to extract and transform nested JSON data into a
        tabular format.

        Args:
            mapping (dict[str, dict[str, str]]): A dictionary where keys are column names and values are dictionaries
            of JSON path expressions. Each JSON path expression specifies how to extract data from the JSON structure
            in the corresponding column.

        Returns:
            DataPointsSearchBuilder: Returns itself to allow for method chaining.
        """
        validate_type(mapping, dict, "Mapping")
        self.mapping = mapping
        return self

    @set_method_call
    def build(self):
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

    def build_execute(self):
        """
        Executes the operations search immediately after building the configuration.

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

    @set_method_call
    def execute(self):
        """
        Executes the datapoints search based on the built configuration.

        Returns:
            dict, csv or  dataframe: The response data in the specified format.

        Raises:
            Exception: If the build() method was not called before execute().
        """
        if not self.builder or self.method_calls[-2] != 'build':
            raise Exception("The build() function must be called and must be the last method invoked before execute")

        query_params = {
            'flattened': self.flatten,
            'utc': self.utc,
            'summary': self.summary,
            'defaultSorted': self.default_sorted,
            'caseSensitive': self.case_sensitive
        }

        url = f'{self.client.url}/north/v80/search/datapoints?{urlencode(query_params)}'
        if self.format_data == 'csv':
            return self.datapoints__csv_request(url)

        return self._datapoints_dict_pandas_request(self.client.headers, url, self.body_data)

    def datapoints__csv_request(self, url: str) -> dict[str, Any] | str | Any:
        try:
            response = send_request(method='post', headers=self.client.headers, url=url, json_payload=self.body_data)

            if response.status_code != 200:
                return handle_error_response(response)

            if not self.transpose or self.mapping is None:
                return response.text

            data_str = StringIO(response.content.decode('utf-8'))
            data = pd.read_csv(data_str, sep=';')

            if self.transpose:
                data = self._transpose_data(data)

            if self.mapping is not None:
                data = self._apply_mapping(data)

            return data.to_csv(index=False)

        except Exception as e:
            return handle_exception(e)

    def _datapoints_dict_pandas_request(self, headers: dict, url: str, body_data: dict) -> Any:
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

                if not data.get('datapoints'):
                    break

                all_results.extend(data['datapoints'])

                if has_limit:
                    break

                start += 1

            except Exception as e:
                return handle_exception(e)

        return self._format_results(all_results)

    def _format_results(self, all_results: list) -> Any:
        if self.format_data in ['dict', None]:
            return all_results

        if self.format_data == 'pandas':
            datapoints_flattened = [flatten(datapoint, reducer='underscore', enumerate_types=(list,)) for datapoint in
                                    all_results]
            return pd.DataFrame(datapoints_flattened)

        raise ValueError(f"Unsupported format: {self.format_data}")

    def _validate_builds(self):
        if self.format_data is not None and all(
                keyword not in self.format_data for keyword in ["csv", "pandas", "dict"]):
            raise Exception(
                'Invalid value for the "with_format" method. Available parameters are only "dict", "csv", and "pandas".')

        if self.format_data != "csv" and (
                self.method_calls.count('with_transpose') > 0 or self.method_calls.count('with_mapped_transpose') > 0
        ):
            raise Exception(
                "You cannot use 'with_transpose()' or 'with_mapped_transpose()' without 'with_format('csv')'."
            )

        if self.method_calls.count('with_transpose') > 0 and self.method_calls.count('with_mapped_transpose') > 0:
            raise Exception("You cannot use with_transpose() together with with_mapped_transpose()")

        if self.method_calls.count('with_format') > 1:
            raise Exception("You cannot use more than one with_format() method")

    @staticmethod
    def _transpose_data(data: pd.DataFrame) -> pd.DataFrame:
        data = data.pivot_table(index=['at', 'entity'], columns='datastream', fill_value=None, aggfunc='first')
        data = data.sort_values(by='at')
        data = data['value']
        data = data.reset_index()
        data = data.infer_objects(copy=False)
        return data

    def _apply_mapping(self, data: pd.DataFrame) -> pd.DataFrame:
        for column, sub_complexdata in self.mapping.items():
            if column in data.columns:
                json_path_expressions = {key: parse(value) for key, value in sub_complexdata.items()}
                for row_index, cell_value in data[column].items():
                    if not pd.isna(cell_value):
                        for key, json_path_expr in json_path_expressions.items():
                            matches = json_path_expr.find(json.loads(cell_value))
                            if matches:
                                new_column = f'{key}'
                                if new_column not in data.columns:
                                    data[new_column] = None
                                data.at[row_index, new_column] = matches[0].value
        return data
