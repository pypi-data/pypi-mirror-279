"""Modulo para testar a função print_requesting_message
em interactive_interface.py"""

from unittest.mock import patch

from encryptdef.interactive_interface import print_requesting_message


def test_print_requesting_message_sucess():
    """Testa a função validate_and_get_input"""
    with (
        patch(
            "encryptdef.interactive_interface.get_user_input",
            return_value="data_test",
        ),
        patch(
            "encryptdef.interactive_interface.print_template_logo"
        ) as mock_template,
    ):

        tuple_data = print_requesting_message(
            "template_message_test", "template_key_test"
        )
        assert tuple_data == ("data_test", "data_test")
        mock_template.assert_called_once()
