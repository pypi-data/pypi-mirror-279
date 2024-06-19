"""Modulo para testar a função print_get_max_workers
em interactive_interface.py"""

from unittest.mock import patch

from encryptdef.interactive_interface import print_get_max_workers
from encryptdef.template import TEMPLATE_ERROR_INVALID_CHOICE


def test_print_get_max_workers_few_lines():
    """Função de teste quando o número de linhas é menor ou igual a 500"""
    lines = ["line"] * 500
    result = print_get_max_workers(lines)
    assert result == 1


@patch("os.cpu_count", return_value=4)
@patch("encryptdef.interactive_interface.console.input", return_value="2")
def test_print_get_max_workers_many_lines_valid_choice(
    mock_cpu_count, mock_input
):  # pylint: disable=W0613
    """Função de testa número de linhas maior que 500"""
    lines = ["line"] * 501
    result = print_get_max_workers(lines)
    assert result == 2


@patch("os.cpu_count", return_value=4)
@patch(
    "encryptdef.interactive_interface.console.input",
    side_effect=["10", "*", " ", "dasd", "d", "E", "-1", "2"],
)
@patch("encryptdef.interactive_interface.print_and_record_log")
def test_print_get_max_workers_many_lines_invalid_choice(
    mock_log, mock_input, mock_cpu_count
):  # pylint: disable=W0613
    """Função de testa se o valor do input é valido"""
    lines = ["line"] * 501
    result = print_get_max_workers(lines)
    assert result == 2
    mock_log.assert_called_with(TEMPLATE_ERROR_INVALID_CHOICE, "error")


@patch("os.cpu_count", return_value=None)
@patch("encryptdef.interactive_interface.console.input", return_value="1")
def test_print_get_max_workers_cpu_count_none(
    mock_cpu_count, mock_input
):  # pylint: disable=W0613
    """Função de teste quando os.cpu_count retorna None"""
    lines = ["line"] * 501
    result = print_get_max_workers(lines)
    assert result == 1
