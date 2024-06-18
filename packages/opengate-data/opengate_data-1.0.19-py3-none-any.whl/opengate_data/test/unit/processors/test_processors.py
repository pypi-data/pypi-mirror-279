""" Unit tests provision bulks """

import pytest

import sys
import os
import configparser
from pprint import pprint
import pandas as pd
from ....opengate_client import OpenGateClient
from ....provision.processor.provision_processor import ProvisionProcessorBuilder


@pytest.fixture
def client():
    return OpenGateClient(url="url", api_key="api_password")


class TestProvisonProcessor:
    """Unit tests for the ProvisionProcessorBuilder functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.builder = ProvisionProcessorBuilder(client)

    def test_with_organization_name(self):
        self.builder.with_organization_name('test_org')
        assert self.builder.organization_name == 'test_org'
        assert isinstance(self.builder.organization_name, str)

    def test_with_identifier(self):
        self.builder.with_identifier('identifier')
        assert self.builder.provision_processor_id == 'identifier'
        assert isinstance(self.builder.provision_processor_id, str)

    def test_with_name(self):
        self.builder.with_name('name')
        assert self.builder.provision_processor_name == 'name'
        assert isinstance(self.builder.provision_processor_name, str)

    def test_with_bulk_process_identitifer(self):
        self.builder.with_bulk_process_identitifer('identifier_process')
        assert self.builder.bulk_process_id == 'identifier_process'
        assert isinstance(self.builder.bulk_process_id, str)

    def test_build_with_build_execute(self):
        self.builder.method_calls = ['build_execute']
        with pytest.raises(Exception):
            self.builder.build()
        assert "You cannot use build() together with build_execute()"

    def test_build_execute_without_build(self):
        self.builder.method_calls = []
        with pytest.raises(Exception):
            self.builder.build_execute()

    def test_build_execute_with_build(self):
        self.builder.method_calls = ['build', 'build_execute']
        self.builder.builder = True
        with pytest.raises(Exception):
            self.builder.build_execute()

    def test_execute_with_incorrect_order(self):
        self.builder.method_calls = ['build', 'with_device_identifier', 'execute']
        with pytest.raises(Exception):
            self.builder.execute()

