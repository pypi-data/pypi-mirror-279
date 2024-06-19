"""Modulo para testar a função encrypt_message em core.py"""

from unittest.mock import patch

from encryptdef.core import encrypt_message
from encryptdef.template import TEMPLATE_ENCRYPTED, TEMPLATE_ENCRYPTED_MESSAGE

ENCRYPT_MESSAGE = "cipher_text*salt*nonce*tag"
CORRECT_KEY = "correct_key"


# Mock das funções que produzem saídas
@patch("encryptdef.core.print_success_message")
@patch("encryptdef.core.print_and_record_log")
def test_encrypt_message_success(
    mock_print_and_record_log, mock_print_success_message
):
    """testar a função encrypt_message"""

    # Mock da função decrypt para retornar a mensagem descriptografada esperada
    with patch("encryptdef.core.encrypt", return_value="encrypt_message"):
        encrypt_message(ENCRYPT_MESSAGE, CORRECT_KEY)

    # Verifica se a mensagem de sucesso foi chamada corretamente
    mock_print_success_message.assert_called_once_with(
        "encrypt_message",
        TEMPLATE_ENCRYPTED_MESSAGE,
        TEMPLATE_ENCRYPTED,
    )

    # Verifica se não houve chamadas de log de erro
    mock_print_and_record_log.assert_not_called()
