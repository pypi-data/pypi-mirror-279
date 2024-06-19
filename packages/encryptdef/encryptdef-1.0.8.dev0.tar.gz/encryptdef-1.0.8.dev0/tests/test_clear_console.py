"""Modulo para testar a função clear_console em utils.py"""

from unittest import mock

from encryptdef.utils import clear_console


@mock.patch("builtins.print")
def test_clear_console_posix(mock_print):
    """Testa a função clear_console em sistemas POSIX"""
    with mock.patch("os.name", "posix"):
        clear_console()
    mock_print.assert_called_once_with("\033[H\033[J", end="")


@mock.patch("builtins.print")
def test_clear_console_nt(mock_print):
    """Testa a função clear_console em sistemas Windows"""
    with mock.patch("os.name", "nt"):
        clear_console()
    mock_print.assert_called_once_with("\033c", end="")
