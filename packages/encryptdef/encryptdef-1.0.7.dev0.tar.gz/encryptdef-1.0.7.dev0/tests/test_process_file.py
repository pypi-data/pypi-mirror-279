""" Modulo para testar a função process_file em core.py"""

import os
from unittest.mock import patch

from encryptdef.core import InvalidEncryptedFormat, InvalidKey, process_file
from encryptdef.template import (
    TEMPLATE_EMPTY_FILE_ERROR,
    TEMPLATE_FILE_NOT_FOUND,
    TEMPLATE_IS_DIRECTORY,
    TEMPLATE_TYPE_ERROR,
)


# Funções de criptografia e descriptografia simuladas para testes
def mock_encrypt(message, key):  # pylint: disable=W0613
    """Função exemplo de encrypt"""
    return f"encrypted-{message}"


def mock_decrypt(message, key):  # pylint: disable=W0613
    """Função exemplo de decrypt"""
    if "invalid" in message:
        raise InvalidKey("Invalid key")
    return f"decrypted-{message}"


def mock_process_line_func_invalid(line, key):  # pylint: disable=W0613
    """Função exemplo de retorno invalido"""
    return 123


def test_process_file_success():
    """Testa a função process_file"""

    # Substitui as funções reais por mocks durante o teste
    with (
        patch("encryptdef.core.read_file") as mock_read_file,
        patch("encryptdef.core.write_file") as mock_write_file,
    ):
        data_list = ["/path/to/file", "key", "new_file"]

        mock_read_file.return_value = ["line1", "line2"]

        assert process_file(data_list, mock_encrypt) is True
        mock_read_file.assert_called_once_with("/path/to/file")
        mock_write_file.assert_called_once_with(
            "new_file", ["encrypted-line1\n", "encrypted-line2\n"]
        )


def test_process_file_file_not_found():
    """Testa a função process_file"""
    with (
        patch("encryptdef.core.console") as mock_console,
        patch("encryptdef.core.print_and_record_log") as mock_log,
        patch("encryptdef.core.read_file", side_effect=FileNotFoundError),
    ):
        data_list = ["/path/to/file", "key", "new_file"]
        assert process_file(data_list, mock_encrypt) is False
        mock_log.assert_called_with(
            TEMPLATE_FILE_NOT_FOUND % "/path/to/file", "error"
        )
        mock_console.print.assert_called()


def test_process_file_invalid_encrypted_format():
    """Testa a função process_file"""
    with (
        patch("encryptdef.core.print_and_record_log") as mock_log,
        patch(
            "encryptdef.core.process_file_content",
            side_effect=InvalidEncryptedFormat("Invalid format"),
        ),
    ):
        data_list = ["/path/to/file", "key", "new_file"]
        assert process_file(data_list, mock_encrypt) is False
        mock_log.assert_called_with("Invalid format", "error")


def test_process_file_invalid_key():
    """Testa a função process_file"""
    with (
        patch("encryptdef.core.print_and_record_log") as mock_log,
        patch("encryptdef.core.read_file", return_value=["invalid"]),
    ):
        data_list = ["/path/to/file", "invalid-key", "new_file"]
        assert process_file(data_list, mock_decrypt) is False
        mock_log.assert_called_with("Invalid key", "error")


def test_process_file_empty_file():
    """Testa a função process_file"""
    with (
        patch("encryptdef.core.print_and_record_log") as mock_log,
        patch("encryptdef.core.read_file", return_value=[]),
    ):
        data_list = ["/path/to/file", "key", "new_file"]
        assert process_file(data_list, mock_decrypt) is False
        mock_log.assert_called_with(
            TEMPLATE_EMPTY_FILE_ERROR % "/path/to/file", "error"
        )


def test_process_file_is_adirectory_error():
    """Testa a função process_file"""
    with patch("encryptdef.core.print_and_record_log") as mock_log:
        current_dir = os.getcwd()
        data_list = [current_dir, "key", "new_file"]
        assert process_file(data_list, mock_decrypt) is False
        mock_log.assert_called_with(
            TEMPLATE_IS_DIRECTORY % current_dir, "error"
        )


def test_process_file_type_error():
    """Testa a função process_file"""
    with (
        patch("encryptdef.core.print_and_record_log") as mock_log,
        patch("encryptdef.core.read_file", return_value=["invalid"]),
    ):
        data_list = ["/path/to/file", "key", "new_file"]
        assert process_file(data_list, mock_process_line_func_invalid) is False
        mock_log.assert_called_with(TEMPLATE_TYPE_ERROR % {type(123)}, "error")
