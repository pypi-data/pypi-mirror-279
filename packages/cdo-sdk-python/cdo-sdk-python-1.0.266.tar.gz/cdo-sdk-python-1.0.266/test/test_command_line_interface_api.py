# coding: utf-8

"""
    CDO API

    Use the documentation to explore the endpoints CDO has to offer

    The version of the OpenAPI document: 0.1.0
    Contact: cdo.tac@cisco.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from cdo_sdk_python.api.command_line_interface_api import CommandLineInterfaceApi


class TestCommandLineInterfaceApi(unittest.TestCase):
    """CommandLineInterfaceApi unit test stubs"""

    def setUp(self) -> None:
        self.api = CommandLineInterfaceApi()

    def tearDown(self) -> None:
        pass

    def test_create_cli_macro(self) -> None:
        """Test case for create_cli_macro

        Create CLI Macro
        """
        pass

    def test_delete_cli_macro(self) -> None:
        """Test case for delete_cli_macro

        Delete CLI Macro
        """
        pass

    def test_get_cli_macro(self) -> None:
        """Test case for get_cli_macro

        Get CLI Macro
        """
        pass

    def test_get_cli_macros(self) -> None:
        """Test case for get_cli_macros

        Get CLI Macros
        """
        pass

    def test_get_cli_result(self) -> None:
        """Test case for get_cli_result

        Get CLI Result
        """
        pass

    def test_get_cli_results(self) -> None:
        """Test case for get_cli_results

        Get CLI Results
        """
        pass

    def test_modify_cli_macro(self) -> None:
        """Test case for modify_cli_macro

        Modify CLI Macro
        """
        pass


if __name__ == '__main__':
    unittest.main()
