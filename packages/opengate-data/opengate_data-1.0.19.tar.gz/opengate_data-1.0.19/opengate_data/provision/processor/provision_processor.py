"""  ProvisionProcessorBuilder """

import requests
from typing import Any
from opengate_data.utils.utils import validate_type, set_method_call
from requests import Response
from opengate_data.utils.utils import validate_type, send_request, set_method_call, handle_basic_response


class ProvisionProcessorBuilder:
    """ Provision Processor operations """

    def __init__(self, opengate_client):
        self.client = opengate_client
        self.headers: dict[str, Any] = self.client.headers
        self.organization_name: str | None = None
        self.provision_processor_id: str | None = None
        self.provision_processor_name: str | None = None
        self.bulk_process_id: str | None = None
        self.bulk_file: str | None = None
        self.url: str | None = None
        self.method: str | None = None
        self.requires: dict[str, Any] = {}
        self.builder: str | None = None
        self.method_calls: list = []

    @set_method_call
    def with_organization_name(self, organization_name: str) -> 'ProvisionProcessorBuilder':
        """
        Specify the organization name.

        Args:
            organization_name (str): The name of the organization.

        Example:
            builder.with_organization_name('organization_name')

        Returns:
            ProvisionProcessorBuilder: Returns self for chaining.
        """
        validate_type(organization_name, str, "Organization")
        self.organization_name = organization_name
        return self

    @set_method_call
    def with_identifier(self, provision_processor_id: str) -> 'ProvisionProcessorBuilder':
        """
         Specify the identifier for the provision processor.

         Args:
             provision_processor_id (str): The identifier for the pipeline.

        Example:
            builder.with_identifier('identifier')

         Returns:
             ProvisionProcessorBuilder: Returns self for chaining.
         """
        validate_type(provision_processor_id, str, "Identifier")
        self.provision_processor_id = provision_processor_id
        return self

    @set_method_call
    def with_name(self, provision_processor_name: str) -> 'ProvisionProcessorBuilder':
        """
         Specify the name for the provision processor.

         Args:
             provision_processor_name (str): The name for the provision processor.

        Example:
            builder.with_name('name')

         Returns:
             ProvisionProcessorBuilder: Returns self for chaining.
         """
        validate_type(provision_processor_name, str, "Name")
        self.provision_processor_name = provision_processor_name
        return self

    @set_method_call
    def with_bulk_file(self, bulk_file: str) -> 'ProvisionProcessorBuilder':
        """
        Specify the file for bulk processing.

        Args:
            bulk_file (str): The path to the file to be uploaded for bulk processing.

        Example:
            builder.with_bulk_file('/path/to/bulk/file.xlsx')

        Returns:
            ProvisionProcessorBuilder: Returns self for chaining.
        """
        self.bulk_file = {'file': (
            'salida.xlsx', open(bulk_file, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
        return self

    @set_method_call
    def with_bulk_process_identitifer(self, bulk_process_id: str) -> 'ProvisionProcessorBuilder':
        """
         Specify the identifier for the bulk process identifier.

         Args:
             bulk_process_id (str): The identifier for the bulk process.

        Example:
            builder.with_bulk_process_identitifer('identifier')

         Returns:
             ProvisionProcessorBuilder: Returns self for chaining.
         """
        self.bulk_process_id = bulk_process_id
        return self

    @set_method_call
    def bulk(self) -> 'ProvisionProcessorBuilder':
        """
        Configure the builder for bulk provisioning.

        This method sets the necessary headers and URL for performing a bulk provisioning operation.

        Example:
            builder.with_organization_name('organization_name') \
                   .with_identifier('identifier') \
                   .with_bulk_file('/path/to/bulk/file.xlsx') \
                   .bulk()

        Returns:
            ProvisionProcessorBuilder: Returns self for chaining.
        """
        self.method = 'bulk_provision_processor'
        self.headers['Accept'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        self.url = f'{self.client.url}/north/v80/provisionProcessors/provision/organizations/{self.organization_name}/{self.provision_processor_id}/bulk'
        return self

    @set_method_call
    def find_by_name(self) -> 'ProvisionProcessorBuilder':
        """
        Configure the builder to find a provision processor by name.

        This method sets the necessary headers and URL for finding a provision processor by its name.

        Example:
            builder.with_organization_name('organization_name') \
                   .with_name('provision_processor_name') \
                   .find_by_name()

        Returns:
            ProvisionProcessorBuilder: Returns self for chaining.
        """
        self.method = 'find_by_name'
        self.headers['Accept'] = 'application/json'
        self.url = f'{self.client.url}/north/v80/provisionProcessors/provision/organizations/{self.organization_name}'
        return self

    @set_method_call
    def bulk_status(self) -> 'ProvisionProcessorBuilder':
        """
        Configure the builder to check the status of a bulk process.

        This method sets the necessary headers and URL for checking the status of a bulk process.

        Example:
            builder.with_organization_name('organization_name') \
                   .with_bulk_process_identitifer('bulk_process_id') \
                   .bulk_status()

        Returns:
            ProvisionProcessorBuilder: Returns self for chaining.
        """
        self.method = 'bulk_status'
        self.headers['Accept'] = 'application/json'
        self.url = f'{self.client.url}/north/v80/provisionProcessors/provision/organizations/{self.organization_name}/bulk/{self.bulk_process_id}'
        return self

    @set_method_call
    def bulk_details(self) -> 'ProvisionProcessorBuilder':
        """
        Configure the builder to get the details of a bulk process.

        This method sets the necessary headers and URL for retrieving the details of a bulk process.

        Example:
            builder.with_organization_name('organization_name') \
                   .with_bulk_process_identitifer('bulk_process_id') \
                   .bulk_details()

        Returns:
            ProvisionProcessorBuilder: Returns self for chaining.
        """
        self.method = 'bulk_details'
        self.headers['Accept'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        self.url = f'{self.client.url}/north/v80/provisionProcessors/provision/organizations/{self.organization_name}/bulk/{self.bulk_process_id}/details'
        return self

    @set_method_call
    def build(self) -> 'ProvisionProcessorBuilder':
        """
        Finalizes the construction of the IoT collection configuration.

        This method prepares the builder to execute the collection by ensuring all necessary configurations are set and validates the overall integrity of the build. It should be called before executing the collection to ensure that the configuration is complete and valid.

        The build process involves checking that mandatory fields such as the device identifier are set. It also ensures that method calls that are incompatible with each other (like `build` and `build_execute`) are not both used.

        Example:
            builder.build()

        Returns:
            ProvisionProcessorBuilder: Returns itself to allow for method chaining, enabling further actions like `execute`.

        Raises:
            ValueError: If required configurations are missing or if incompatible methods are used together.

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

        self._validate_builds()
        return self.execute()

    def execute(self) -> requests.Response:
        """
        Execute the configured operation and return the response.

        This method executes the operation that has been configured using the builder pattern. It ensures that the `build` method has been called and that it is the last method invoked before `execute`. Depending on the configured method (e.g., create, find, update, delete), it calls the appropriate internal execution method.

        Returns:
            requests.Response: The response object from the executed request.

        Raises:
            Exception: If the `build` method has not been called or if it is not the last method invoked before `execute`.
            ValueError: If the configured method is unsupported.
        """
        methods = {
            'bulk_provision_processor': self._execute_bulk,
            'find_by_name': self._execute_find_by_name,
            'bulk_status': self._execute_bulk_status,
            'bulk_details': self._execute_bulk_details,
        }
        function = methods.get(self.method)
        if function is None:
            raise ValueError(f'Unsupported method: {self.method}')
        return function()

    def _execute_bulk(self) -> dict[str, Any]:
        send_request(method='post', headers=self.headers, url=self.url, files=self.bulk_file)
        return handle_basic_response(response)

    def _execute_find_by_name(self):
        request_response = send_request(method="get", headers=self.headers, url=self.url)
        data = request_response.json()
        provision_procesor = {}
        for item in data.get("provisionProcessors", []):
            if item.get("name") == self.provision_processor_name:
                provision_procesor = item
        return provision_procesor

    def _execute_bulk_status(self) -> dict[str, Any] | Any:
        response = send_request(method="get", headers=self.headers, url=self.url)
        if response.status_code == 200:
            return response
        else:
            return {'status_code': response.status_code, 'error': response.text}

    def _execute_bulk_details(self) -> dict[str, Any] | Response | Any:
        response = send_request(method="get", headers=self.headers, url=self.url)
        if response.status_code == 200:
            return response
        else:
            return {'status_code': response.status_code, 'error': response.text}

    def _validate_builds(self):
        required_methods = {
            'bulk': ['with_organization_name', 'with_identifier', 'with_bulk_file', 'with_bulk_file'],
            'find_by_name': ['with_organization_name', 'with_name'],
            'bulk_status': ['with_organization_name', 'with_bulk_process_identitifer'],
            'bulk_datails': ['with_organization_name', 'with_bulk_process_identitifer']
        }
        for method, required in required_methods.items():
            if self.method_calls.count(method) > 0:
                missing_methods = [req for req in required if req not in self.method_calls]
                if missing_methods:
                    raise Exception(f"It is mandatory to use the {', '.join(missing_methods)} method(s) in {method}()")
        return self
