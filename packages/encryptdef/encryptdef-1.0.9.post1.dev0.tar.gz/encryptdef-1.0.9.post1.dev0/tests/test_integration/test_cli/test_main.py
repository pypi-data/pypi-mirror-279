"""Modulo para testar a função main em cli.py"""

from unittest.mock import patch

import pytest
from click.testing import CliRunner

from encryptdef.cli import main


@pytest.fixture(name="runner")
def runner_fixture():
    """Função fixture para teste"""
    return CliRunner()


@patch("encryptdef.core.interactive_mode")
def test_main_no_command(mock_interactive, runner):
    """Teste para a função main sem nenhum subcomando."""
    result = runner.invoke(main)
    assert result.exit_code == 0
    mock_interactive.assert_called_once()


def test_main_command_help(runner):
    """Teste para o comando encrypt --help"""
    result = runner.invoke(main, ["encrypt", "--help"])
    assert result.exit_code == 0
    assert "OPTIONS" in result.output
    assert "encrypt" in result.output
    assert "--message" in result.output
    assert "--file" in result.output
