"""Modulo para testar a função decrypt_message em core.py"""

from unittest.mock import patch

from encryptdef.core import (
    TEMPLATE_DECRYPTED,
    TEMPLATE_DECRYPTED_MESSAGE,
    InvalidEncryptedFormat,
    InvalidKey,
    decrypt_message,
)

ENCRYPT_MESSAGE = "cipher_text*salt*nonce*tag"
CORRECT_KEY = "correct_key"
WRONG_KEY = "wrong_key"


# Mock das funções que produzem saídas
@patch("encryptdef.core.print_success_message")
@patch("encryptdef.core.print_and_record_log")
def test_decrypt_message_success(
    mock_print_and_record_log, mock_print_success_message
):
    """testar a função decrypt_message"""

    # Mock da função decrypt para retornar a mensagem descriptografada esperada
    with patch("encryptdef.core.decrypt", return_value="decrypted_message"):
        result = decrypt_message(ENCRYPT_MESSAGE, CORRECT_KEY)

    # Verifica se o resultado é True
    assert result is True

    # Verifica se a mensagem de sucesso foi chamada corretamente
    mock_print_success_message.assert_called_once_with(
        "decrypted_message",
        TEMPLATE_DECRYPTED_MESSAGE,
        TEMPLATE_DECRYPTED,
    )

    # Verifica se não houve chamadas de log de erro
    mock_print_and_record_log.assert_not_called()


@patch("encryptdef.core.print_success_message")
@patch("encryptdef.core.print_and_record_log")
def test_decrypt_message_invalid_key(
    mock_print_and_record_log, mock_print_success_message
):
    """testar a função decrypt_message"""

    # Mock da função decrypt para levantar um InvalidKey
    with patch("encryptdef.core.decrypt", side_effect=InvalidKey):
        result = decrypt_message(ENCRYPT_MESSAGE, WRONG_KEY)

    # Verifica se o resultado é False
    assert result is False

    # Verifica se o log de erro foi chamado
    mock_print_and_record_log.assert_called_once()

    # Verifica se a mensagem de sucesso não foi chamada
    mock_print_success_message.assert_not_called()


@patch("encryptdef.core.print_success_message")
@patch("encryptdef.core.print_and_record_log")
def test_decrypt_message_invalid_format(
    mock_print_and_record_log, mock_print_success_message
):
    """testar a função decrypt_message"""

    # Mock da função decrypt para levantar um InvalidEncryptedFormat
    with patch("encryptdef.core.decrypt", side_effect=InvalidEncryptedFormat):
        result = decrypt_message("invalid_format", CORRECT_KEY)

    # Verifica se o resultado é False
    assert result is False

    # Verifica se o log de erro foi chamado
    mock_print_and_record_log.assert_called_once()

    # Verifica se a mensagem de sucesso não foi chamada
    mock_print_success_message.assert_not_called()
