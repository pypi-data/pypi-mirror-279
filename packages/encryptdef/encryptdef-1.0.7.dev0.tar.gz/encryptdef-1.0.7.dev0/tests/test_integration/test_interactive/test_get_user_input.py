"""Modulo para testar a função get_user_input em interactive_interface.py"""

from unittest.mock import patch

from encryptdef.interactive_interface import get_user_input


def test_get_user_input_sucess():
    """Testa a função print_template_logo"""
    with (
        patch("encryptdef.interactive_interface.console.input") as mock_input,
    ):
        prompt_test = "test"
        password_test = True
        get_user_input(prompt_test, password_test)

        mock_input.assert_called_with("test", password=True)
