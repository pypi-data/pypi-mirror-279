"""Modulo para testar a função print_template_logo
em interactive_interface.py"""

from unittest.mock import patch

import pytest

from encryptdef.interactive_interface import print_template_logo
from encryptdef.template import TEMPLATE_INFO, TEMPLATE_LOGO


@pytest.fixture(name="mock_console_print")
def mock_console_print_fixture():
    """Função fixture para teste"""
    with patch("encryptdef.interactive_interface.console.print") as mock_input:
        yield mock_input


@pytest.fixture(name="mock_clear_console")
def mock_clear_console_fixture():
    """Função fixture para teste"""
    with patch("encryptdef.interactive_interface.clear_console") as mock_clear:
        yield mock_clear


@pytest.fixture(name="mock_markdown")
def mock_markdown_fixture():
    """Função fixture para teste"""
    with patch("encryptdef.interactive_interface.Markdown") as mock_mark:
        yield mock_mark


def test_print_template_logo_default(mock_clear_console, mock_console_print):
    """Testa a função print_template_logo"""

    # Teste quando info é False
    print_template_logo(info=False)

    # Assegura que clear_console foi chamado
    mock_clear_console.assert_called_once()

    # Assegura que TEMPLATE_LOGO foi impresso
    mock_console_print.assert_called_once_with(TEMPLATE_LOGO)


def test_print_template_logo_with_info(
    mock_markdown, mock_clear_console, mock_console_print
):
    """Testa a função print_template_logo"""

    # Mock do objeto Markdown
    mock_md = mock_markdown.return_value

    # Teste quando info é True
    print_template_logo(info=True)

    # Assegura que clear_console foi chamado
    mock_clear_console.assert_called_once()

    # Assegura que TEMPLATE_LOGO foi impresso
    mock_console_print.assert_any_call(TEMPLATE_LOGO)

    # Assegura que TEMPLATE_INFO foi transformado em Markdown
    mock_markdown.assert_called_once_with(TEMPLATE_INFO)

    # Assegura que o Markdown foi impresso
    mock_console_print.assert_any_call(mock_md)
