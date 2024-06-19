"""Modulo para testar a função print_requesting_file
em interactive_interface.py"""

from unittest.mock import patch

from encryptdef.interactive_interface import print_requesting_file
from encryptdef.template import TEMPLATE_DECRYPT_FILE, TEMPLATE_ENCRYPT_FILE


def test_print_requesting_file_encrypt_sucess():
    """Testa a função print_requesting_file"""
    with (
        patch(
            "encryptdef.interactive_interface.get_user_input",
            return_value="data_test",
        ),
        patch(
            "encryptdef.interactive_interface.print_template_logo"
        ) as mock_template,
    ):

        tuple_data = print_requesting_file(TEMPLATE_ENCRYPT_FILE)
        mock_template.assert_called_once()
        assert tuple_data == ["data_test", "data_test", "data_test"]


def test_print_requesting_file_decrypt_sucess():
    """Testa a função print_requesting_file"""
    with (
        patch(
            "encryptdef.interactive_interface.get_user_input",
            return_value="data_test",
        ),
        patch(
            "encryptdef.interactive_interface.print_template_logo"
        ) as mock_template,
    ):

        tuple_data = print_requesting_file(TEMPLATE_DECRYPT_FILE)
        mock_template.assert_called_once()
        assert tuple_data == ["data_test", "data_test", "data_test"]
