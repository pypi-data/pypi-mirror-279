"""Modulo para testar a função encrypt em cli.py"""

from unittest.mock import patch

import pytest
from click.testing import CliRunner

from encryptdef import core
from encryptdef.cli import main
from encryptdef.template import TEMPLATE_ENCRYPT_KEY


@pytest.fixture(name="runner")
def runner_fixture():
    """Função fixture para teste"""
    return CliRunner()


@patch("encryptdef.cli.core.encrypt_message")
@patch("encryptdef.cli.core.process_keyfile_and_args", return_value="mock_key")
def test_encrypt_command_with_message(
    mock_process_keyfile, mock_encrypt_message, runner
):
    """Teste para o comando encrypt com uma mensagem."""

    result = runner.invoke(main, ["encrypt", "--message", "hello world"])
    assert result.exit_code == 0
    mock_process_keyfile.assert_called_once_with(
        None, "hello world", None, TEMPLATE_ENCRYPT_KEY
    )
    mock_encrypt_message.assert_called_once_with("hello world", "mock_key")


@patch("encryptdef.cli.core.process_file")
@patch("encryptdef.cli.assigning_a_name_file", return_value="encrypt-test.txt")
@patch("encryptdef.cli.core.process_keyfile_and_args", return_value="mock_key")
def test_encrypt_command_with_file(
    mock_process_keyfile,
    mock_assigning,
    mock_process_file,
    runner,
):
    """Teste para o comando encrypt com um arquivo."""

    result = runner.invoke(main, ["encrypt", "--file", "test.txt"])
    assert result.exit_code == 0
    mock_process_keyfile.assert_called_once_with(
        None, None, "test.txt", TEMPLATE_ENCRYPT_KEY
    )
    mock_assigning.assert_called_once_with("test.txt", "encrypt-")
    mock_process_file.assert_called_once_with(
        ["test.txt", "mock_key", "encrypt-test.txt"], core.encrypt
    )


@patch("encryptdef.cli.core.process_file")
@patch("encryptdef.cli.assigning_a_name_file", return_value="encrypt-test.txt")
@patch(
    "encryptdef.cli.core.process_keyfile_and_args",
    return_value="mock_key_file",
)
def test_encrypt_command_with_file_with_keyfile(
    mock_process_keyfile,
    mock_assigning,
    mock_process_file,
    runner,
):
    """Teste para o comando encrypt com um arquivo e keyfile"""

    result = runner.invoke(
        main, ["encrypt", "--keyfile", "key.txt", "--file", "test.txt"]
    )
    assert result.exit_code == 0
    mock_process_keyfile.assert_called_once_with(
        "key.txt", None, "test.txt", TEMPLATE_ENCRYPT_KEY
    )
    mock_assigning.assert_called_once_with("test.txt", "encrypt-")
    mock_process_file.assert_called_once_with(
        ["test.txt", "mock_key_file", "encrypt-test.txt"], core.encrypt
    )
