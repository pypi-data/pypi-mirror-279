"""Modulo para testar a função print_continue_or_leave
em interactive_interface.py"""

from unittest.mock import patch

from encryptdef.interactive_interface import print_continue_or_leave


def test_print_continue_or_leave_sucess():
    """Testa a função print_continue_or_leave"""
    with (
        patch("encryptdef.interactive_interface.get_user_input") as mock_input,
    ):
        template_test = "template test"
        print_continue_or_leave(template_test)

        mock_input.assert_called_with("template test")
