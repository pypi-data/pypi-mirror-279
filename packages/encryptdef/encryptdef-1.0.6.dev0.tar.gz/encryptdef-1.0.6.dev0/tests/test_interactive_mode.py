"""Modulo para testar a função interactive_mode em core.py"""

from unittest.mock import patch

import pytest

from encryptdef.core import decrypt, encrypt, interactive_mode
from encryptdef.template import (
    TEMPLATE_DECRYPT_FILE,
    TEMPLATE_DECRYPT_KEY,
    TEMPLATE_DECRYPT_MESSAGE,
    TEMPLATE_ENCRYPT_FILE,
    TEMPLATE_ENCRYPT_KEY,
    TEMPLATE_ENCRYPT_MESSAGE,
)


@pytest.fixture(name="mock_console_input")
def mock_console_input_fixture():
    """Função fixture para teste"""
    with patch("encryptdef.core.console.input") as mock_input:
        yield mock_input


@pytest.fixture(name="mock_print_request_menu")
def mock_print_request_menu_fixture():
    """Função fixture para teste"""
    with patch("encryptdef.core.print_request_menu") as mock_menu:
        yield mock_menu


@pytest.fixture(name="mock_print_requesting_message")
def mock_print_requesting_message_fixture():
    """Função fixture para teste"""
    with patch("encryptdef.core.print_requesting_message") as mock_message:
        yield mock_message


@pytest.fixture(name="mock_print_requesting_file")
def mock_print_requesting_file_fixture():
    """Função fixture para teste"""
    with patch("encryptdef.core.print_requesting_file") as mock_file:
        yield mock_file


@pytest.fixture(name="mock_encrypt_message")
def mock_encrypt_message_fixture():
    """Função fixture para teste"""
    with patch("encryptdef.core.encrypt_message") as mock_encrypt:
        yield mock_encrypt


@pytest.fixture(name="mock_decrypt_message")
def mock_decrypt_message_fixture():
    """Função fixture para teste"""
    with patch("encryptdef.core.decrypt_message") as mock_decrypt:
        yield mock_decrypt


@pytest.fixture(name="mock_process_file")
def mock_process_file_fixture():
    """Função fixture para teste"""
    with patch("encryptdef.core.process_file") as mock_process:
        yield mock_process


@pytest.fixture(name="mock_print_continue_or_leave")
def mock_print_continue_or_leave_fixture():
    """Função fixture para teste"""
    with patch("encryptdef.core.print_continue_or_leave") as mock_continue:
        yield mock_continue


def test_encrypt_message(
    mock_print_request_menu,
    mock_print_requesting_message,
    mock_encrypt_message,
    mock_print_continue_or_leave,
):
    """Testa a função interactive_mode"""

    # Escolha criptografar mensagem
    mock_print_request_menu.side_effect = [1, 1]
    mock_print_requesting_message.return_value = (
        "Mensagem de Teste",
        "SenhaDeTeste",
    )
    # Termina após uma iteração
    mock_print_continue_or_leave.return_value = True

    interactive_mode()

    mock_print_request_menu.assert_called()
    mock_print_requesting_message.assert_called_once_with(
        TEMPLATE_ENCRYPT_MESSAGE, TEMPLATE_ENCRYPT_KEY
    )
    mock_encrypt_message.assert_called_once_with(
        "Mensagem de Teste", "SenhaDeTeste"
    )


def test_decrypt_message(
    mock_print_request_menu,
    mock_print_requesting_message,
    mock_decrypt_message,
    mock_print_continue_or_leave,
):
    """Testa a função interactive_mode"""

    mock_print_request_menu.side_effect = [1, 2]
    mock_print_requesting_message.return_value = (
        "Mensagem Criptografada",
        "SenhaDeTeste",
    )
    mock_print_continue_or_leave.return_value = True

    interactive_mode()

    mock_print_request_menu.assert_called()
    mock_print_requesting_message.assert_called_once_with(
        TEMPLATE_DECRYPT_MESSAGE, TEMPLATE_DECRYPT_KEY
    )
    mock_decrypt_message.assert_called_once_with(
        "Mensagem Criptografada", "SenhaDeTeste"
    )


def test_encrypt_file(
    mock_print_request_menu,
    mock_print_requesting_file,
    mock_process_file,
    mock_print_continue_or_leave,
):
    """Testa a função interactive_mode"""
    mock_print_request_menu.side_effect = [2, 1]
    mock_print_requesting_file.return_value = ["file_path", "key", "new_file"]
    mock_print_continue_or_leave.return_value = True

    interactive_mode()

    mock_print_request_menu.assert_called()
    mock_print_requesting_file.assert_called_once_with(TEMPLATE_ENCRYPT_FILE)
    mock_process_file.assert_called_once_with(
        ["file_path", "key", "new_file"], encrypt
    )


def test_decrypt_file(
    mock_print_request_menu,
    mock_print_requesting_file,
    mock_process_file,
    mock_print_continue_or_leave,
):
    mock_print_request_menu.side_effect = [2, 2]
    mock_print_requesting_file.return_value = ["file_path", "key", "new_file"]
    mock_print_continue_or_leave.return_value = True

    interactive_mode()

    mock_print_request_menu.assert_called()
    mock_print_requesting_file.assert_called_once_with(TEMPLATE_DECRYPT_FILE)
    mock_process_file.assert_called_once_with(
        ["file_path", "key", "new_file"], decrypt
    )
