"""Modulo para testar a função process_file_content em core.py"""

from unittest.mock import patch

import pytest

from encryptdef.core import (
    EmptyFileError,
    decrypt,
    encrypt,
    process_file_content,
)
from encryptdef.template import (
    TEMPLATE_DECRYPTED_FILE,
    TEMPLATE_ENCRYPTED_FILE,
)


def process_lines_func(x, y):  # pylint: disable=W0613
    """Simula função de processamento de linha"""
    return x


def test_process_file_content_success():
    """Testa a função process_file_content"""

    # Substitui as funções reais por mocks durante o teste
    with (
        patch("encryptdef.core.read_file") as mock_read_file,
        patch("encryptdef.core.print_get_max_workers") as mock_get_max_workers,
        patch("encryptdef.core.process_lines") as mock_process_lines,
        patch("encryptdef.core.write_file") as mock_write_file,
        patch("encryptdef.core.print_and_record_log") as mock_log,
    ):

        # Simula a leitura de um arquivo
        mock_read_file.return_value = ["line1\n", "line2\n"]

        # Simula o cálculo de trabalhadores máximos
        mock_get_max_workers.return_value = 2

        # Simula o processamento das linhas, retornando linhas processadas
        mock_process_lines.return_value = [
            "encrypted_line1\n",
            "encrypted_line2\n",
        ]
        result = process_file_content(
            "testfile.txt", "key", "newfile.txt", process_lines_func
        )

        assert result is True

        # Verifica se read_file foi chamado com o argumento 'testfile.txt'
        mock_read_file.assert_called_once_with("testfile.txt")
        mock_get_max_workers.assert_called_once()

        # Verifica se process_lines foi chamado uma vez com os argumentos
        mock_process_lines.assert_called_once_with(
            ["line1\n", "line2\n"], "key", process_lines_func, 2
        )
        mock_write_file.assert_called_once_with(
            "newfile.txt", ["encrypted_line1\n", "encrypted_line2\n"]
        )

        # Verifica se print_and_record_log foi chamado uma vez
        mock_log.assert_called_once()


def test_process_file_content_empty_file():
    """Testa a função process_file_content"""
    with patch("encryptdef.core.read_file") as mock_read_file:
        mock_read_file.return_value = []

        with pytest.raises(EmptyFileError):
            process_file_content(
                "testfile.txt", "key", "newfile.txt", lambda x, y: x
            )


def test_process_file_content_multithreading():
    """Testa a função process_file_content"""
    with (
        patch("encryptdef.core.read_file") as mock_read_file,
        patch("encryptdef.core.print_get_max_workers") as mock_get_max_workers,
        patch("encryptdef.core.process_lines") as mock_process_lines,
        patch("encryptdef.core.write_file") as mock_write_file,
    ):

        mock_read_file.return_value = [
            "line1\n",
            "line2\n",
            "line3\n",
            "line4\n",
        ]
        mock_get_max_workers.return_value = 4
        mock_process_lines.return_value = [
            "processed_line1\n",
            "processed_line2\n",
            "processed_line3\n",
            "processed_line4\n",
        ]

        result = process_file_content(
            "testfile.txt", "key", "newfile.txt", process_lines_func
        )

        assert result is True
        mock_read_file.assert_called_once_with("testfile.txt")
        mock_get_max_workers.assert_called_once()
        mock_process_lines.assert_called_once_with(
            ["line1\n", "line2\n", "line3\n", "line4\n"],
            "key",
            process_lines_func,
            4,
        )
        mock_write_file.assert_called_once_with(
            "newfile.txt",
            [
                "processed_line1\n",
                "processed_line2\n",
                "processed_line3\n",
                "processed_line4\n",
            ],
        )


def test_process_file_content_log_encrypt():
    """Testa a função process_file_content"""
    with (
        patch("encryptdef.core.read_file") as mock_read_file,
        patch("encryptdef.core.print_get_max_workers") as mock_get_max_workers,
        patch("encryptdef.core.process_lines") as mock_process_lines,
        patch("encryptdef.core.write_file"),
        patch("encryptdef.core.print_and_record_log") as mock_log,
    ):

        mock_read_file.return_value = ["line1\n", "line2\n"]
        mock_get_max_workers.return_value = 2
        mock_process_lines.return_value = [
            "encrypted_line1\n",
            "encrypted_line2\n",
        ]

        process_line_func = encrypt
        result = process_file_content(
            "testfile.txt", "key", "newfile.txt", process_line_func
        )

        assert result is True
        expected_log_message = TEMPLATE_ENCRYPTED_FILE % "newfile.txt"
        mock_log.assert_called_with(expected_log_message, "debug")


def test_process_file_content_log_decrypt():
    """Testa a função process_file_content"""
    with (
        patch("encryptdef.core.read_file") as mock_read_file,
        patch("encryptdef.core.print_get_max_workers") as mock_get_max_workers,
        patch("encryptdef.core.process_lines") as mock_process_lines,
        patch("encryptdef.core.write_file"),
        patch("encryptdef.core.print_and_record_log") as mock_log,
    ):

        mock_read_file.return_value = ["line1\n", "line2\n"]
        mock_get_max_workers.return_value = 2
        mock_process_lines.return_value = [
            "decrypted_line1\n",
            "decrypted_line2\n",
        ]

        process_line_func = decrypt
        result = process_file_content(
            "testfile.txt", "key", "newfile.txt", process_line_func
        )

        assert result is True
        expected_log_message = TEMPLATE_DECRYPTED_FILE % "newfile.txt"
        mock_log.assert_called_with(expected_log_message, "debug")
