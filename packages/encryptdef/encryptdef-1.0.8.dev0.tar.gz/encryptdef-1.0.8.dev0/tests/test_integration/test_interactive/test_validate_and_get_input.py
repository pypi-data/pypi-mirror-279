"""Modulo para testar a função validate_and_get_input
em interactive_interface.py"""

from unittest.mock import patch

from encryptdef.interactive_interface import validate_and_get_input
from encryptdef.template import (
    TEMPLATE_ENCRYPT_FILE,
    TEMPLATE_ENCRYPT_KEY,
    TEMPLATE_ENCRYPT_MESSAGE,
    TEMPLATE_ERROR_EMPTY_FIELD,
)


def test_validate_and_get_input_valid():
    """Testa a função validate_and_get_input"""

    # Mockando a função get_user_input para retornar entradas válidas
    with patch(
        "encryptdef.interactive_interface.get_user_input",
        side_effect=["message", "password123"],
    ):
        prompts = [TEMPLATE_ENCRYPT_MESSAGE, TEMPLATE_ENCRYPT_KEY]
        # Chama a função verificando se as entradas são retornadas corretamente
        inputs = validate_and_get_input(prompts)
        assert inputs == ["message", "password123"]


def test_validate_and_get_input_empty_field():
    """Testa a função validate_and_get_input"""

    with (
        patch(
            "encryptdef.interactive_interface.get_user_input",
            side_effect=[
                "",
                "password123",
                "new_file",
                "file",
                "password123",
                "new_file",
            ],
        ),
        patch(
            "encryptdef.interactive_interface.print_and_record_log"
        ) as mock_log,
        patch("encryptdef.interactive_interface.clear_console") as mock_clear,
        patch(
            "encryptdef.interactive_interface.print_template_logo"
        ) as mock_template,
    ):

        inputs = validate_and_get_input(TEMPLATE_ENCRYPT_FILE.split("\n"))
        assert inputs == ["file", "password123", "new_file"]
        mock_clear.assert_called()
        mock_template.assert_called()
        mock_log.assert_called_with(TEMPLATE_ERROR_EMPTY_FIELD, "error")
