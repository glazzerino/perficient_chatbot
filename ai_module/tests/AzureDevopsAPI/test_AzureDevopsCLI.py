from unittest.mock import Mock, patch, MagicMock
import unittest
from ai_module.src.llm_tools.AzureDevopsAPI_Tool import (
    _jmespath_filter,
    _check_args,
    get_projects,
    azure_devops_cli,
)


class TestAzureDevopsCLI(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_jmespath_filter_success(self):
        data = {"key": "value", "key2": "value2"}
        query = "key"
        expected_output = "value"
        actual_output = _jmespath_filter(data, query)
        self.assertEqual(expected_output, actual_output)

    def test_jmespath_filter_empty_query(self):
        data = {"key": "value"}
        query = ""
        expected_output = {"key": "value"}
        actual_output = _jmespath_filter(data, query)
        self.assertEqual(expected_output, actual_output)

    def test_check_args_success(self):
        args = ["arg1", "arg2"]
        checks = ["arg1", "arg2"]
        self.assertIsNone(_check_args(checks, args))

    def test_check_args_missing_arg(self):
        args = ["arg2"]
        checks = ["arg1", "arg2"]
        with self.assertRaises(Exception):
            _check_args(checks, args)

    def test_check_args_no_args(self):
        with self.assertRaises(Exception):
            _check_args(None)

    @patch("ai_module.src.utils.AzureDevops.AzureDevopsAPI")
    def test_get_projects_success(self, mock_azure_devops_api):
        # Given
        expected_output = ["project1", "project2"]
        get_projects.return_value = expected_output
        mock_azure_devops_api.get_projects.return_value = expected_output

        # When
        actual_output = get_projects(mock_azure_devops_api, {"project": "projectName"})

        # Then
        self.assertEqual(expected_output, actual_output)

    # @patch("src.utils.AzureDevops.AzureDevopsAPI")
    def test_help_command_output_not_empty(self):
        # Given
        command = "help"

        # When
        actual_output = azure_devops_cli(command, token="token", org="org")

        # Then
        self.assertIsNotNone(actual_output)
