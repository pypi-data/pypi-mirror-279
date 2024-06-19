"""Modulo para testar a função print_success_message
em interactive_interface.py"""

from unittest.mock import patch

from encryptdef.interactive_interface import print_success_message
from encryptdef.template import (
    TEMPLATE_DECRYPTED,
    TEMPLATE_DECRYPTED_MESSAGE,
    TEMPLATE_ENCRYPTED,
    TEMPLATE_ENCRYPTED_MESSAGE,
)


def test_print_sucess_message_template_encrypt():
    """Testa a função validate_and_get_input"""
    with (
        patch(
            "encryptdef.interactive_interface.print_and_record_log"
        ) as mock_log,
    ):
        message = "encrypt message test"
        print_success_message(
            message, TEMPLATE_ENCRYPTED_MESSAGE, TEMPLATE_ENCRYPTED
        )

        mock_log.assert_any_call(TEMPLATE_ENCRYPTED_MESSAGE, "debug")
        mock_log.assert_any_call(TEMPLATE_ENCRYPTED % message, "debug")

        mock_log.call_count = 2


def test_print_sucess_message_template_decrypt():
    """Testa a função validate_and_get_input"""
    with (
        patch(
            "encryptdef.interactive_interface.print_and_record_log"
        ) as mock_log,
    ):
        message = "encrypt message test"
        print_success_message(
            message, TEMPLATE_DECRYPTED_MESSAGE, TEMPLATE_DECRYPTED
        )

        mock_log.assert_any_call(TEMPLATE_DECRYPTED_MESSAGE, "debug")
        mock_log.assert_any_call(TEMPLATE_DECRYPTED % message, "debug")

        mock_log.call_count = 2
