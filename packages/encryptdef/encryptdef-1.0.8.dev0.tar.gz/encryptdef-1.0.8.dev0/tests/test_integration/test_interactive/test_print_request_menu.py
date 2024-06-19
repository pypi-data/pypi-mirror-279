"""Modulo para testar a função print_request_menu
em interactive_interface.py"""

from unittest.mock import patch

import pytest

from encryptdef.interactive_interface import print_request_menu
from encryptdef.template import (
    TEMPLATE_ERROR_INVALID_CHOICE,
    TEMPLATE_MENU_ENCRYPT_DECRYPT,
    TEMPLATE_MENU_MESSAGE_FILE,
)


@pytest.fixture(name="mock_print_template_logo")
def mock_print_template_logo_fixture():
    """Função fixture para teste"""
    with patch(
        "encryptdef.interactive_interface.print_template_logo"
    ) as mock_logo:
        yield mock_logo


@pytest.fixture(name="mock_console_input")
def mock_console_input_fixture():
    """Função fixture para teste"""
    with patch("encryptdef.interactive_interface.console.input") as mock_input:
        yield mock_input


@pytest.fixture(name="mock_console_print")
def mock_console_print_fixture():
    """Função fixture para teste"""
    with patch("encryptdef.interactive_interface.console.print") as mock_print:
        yield mock_print


@pytest.fixture(name="mock_clear_console")
def mock_clear_console_fixture():
    """Função fixture para teste"""
    with patch("encryptdef.interactive_interface.clear_console") as mock_clear:
        yield mock_clear


@pytest.fixture(name="mock_print_and_record_log")
def mock_print_and_record_log_fixture():
    """Função fixture para teste"""
    with patch(
        "encryptdef.interactive_interface.print_and_record_log"
    ) as mock_log:
        yield mock_log


def test_print_request_menu_valid_choice(
    mock_print_template_logo,
    mock_console_input,
    mock_console_print,
):
    """Testa a função print_request_menu"""

    mock_console_input.return_value = "1"

    # Chamando a função e verificando se a escolha retornada é correta
    choice = print_request_menu(TEMPLATE_MENU_MESSAGE_FILE)
    assert choice == 1

    # Verificando se as funções foram chamadas
    mock_print_template_logo.assert_called_with(info=True)
    mock_console_print.assert_any_call(TEMPLATE_MENU_MESSAGE_FILE)


def test_print_request_menu_exit_choice(
    mock_print_template_logo,
    mock_console_input,
    mock_console_print,
):
    """Testa a função print_request_menu"""

    mock_console_input.return_value = "3"

    with pytest.raises(SystemExit):
        print_request_menu(TEMPLATE_MENU_MESSAGE_FILE)

        # Verificando se a função foi chamada
        mock_print_template_logo.assert_called_with(info=True)
        mock_console_print.assert_any_call(TEMPLATE_MENU_MESSAGE_FILE)


def test_print_request_menu_invalid_choice(
    mock_clear_console,
    mock_print_and_record_log,
    mock_print_template_logo,
    mock_console_input,
    mock_console_print,
):
    """Testa a função print_request_menu"""
    mock_console_input.side_effect = ["0", "4", "-1", "10", "2"]

    # Chamando a função e verificando se a escolha retornada é correta
    choice = print_request_menu(TEMPLATE_MENU_ENCRYPT_DECRYPT)
    assert choice == 2

    # Verificando se as funções foram chamadas
    assert mock_clear_console.call_count == 4
    assert mock_print_template_logo.call_count == 5
    mock_print_template_logo.assert_called_with(info=True)
    mock_print_and_record_log.assert_called_with(
        TEMPLATE_ERROR_INVALID_CHOICE, "error"
    )
    mock_console_print.assert_any_call(TEMPLATE_MENU_ENCRYPT_DECRYPT)
