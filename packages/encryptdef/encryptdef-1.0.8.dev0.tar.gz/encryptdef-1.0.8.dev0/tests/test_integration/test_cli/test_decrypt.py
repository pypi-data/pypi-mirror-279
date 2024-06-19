"""Modulo para testar a função decrypt em cli.py"""

from unittest.mock import patch

import pytest
from click.testing import CliRunner

from encryptdef import core
from encryptdef.cli import main
from encryptdef.template import TEMPLATE_DECRYPT_KEY


@pytest.fixture(name="runner")
def runner_fixture():
    """Função fixture para teste"""
    return CliRunner()


@patch("encryptdef.cli.core.decrypt_message")
@patch("encryptdef.cli.core.process_keyfile_and_args", return_value="mock_key")
def test_encrypt_command_with_message(
    mock_process_keyfile, mock_decrypt_message, runner
):
    """Teste para o comando decrypt com uma mensagem."""

    result = runner.invoke(
        main, ["decrypt", "--message", "encrypt-helloworld"]
    )
    assert result.exit_code == 0
    mock_process_keyfile.assert_called_once_with(
        None, "encrypt-helloworld", None, TEMPLATE_DECRYPT_KEY
    )
    mock_decrypt_message.assert_called_once_with(
        "encrypt-helloworld", "mock_key"
    )


@patch("encryptdef.cli.core.process_file")
@patch("encryptdef.cli.assigning_a_name_file", return_value="decrypt-test.txt")
@patch("encryptdef.cli.core.process_keyfile_and_args", return_value="mock_key")
def test_encrypt_command_with_file(
    mock_process_keyfile,
    mock_assigning,
    mock_process_file,
    runner,
):
    """Teste para o comando decrypt com um arquivo."""

    result = runner.invoke(main, ["decrypt", "--file", "encrypt-test.txt"])
    assert result.exit_code == 0
    mock_process_keyfile.assert_called_once_with(
        None, None, "encrypt-test.txt", TEMPLATE_DECRYPT_KEY
    )
    mock_assigning.assert_called_once_with("encrypt-test.txt", "decrypt-")
    mock_process_file.assert_called_once_with(
        ["encrypt-test.txt", "mock_key", "decrypt-test.txt"], core.decrypt
    )


@patch("encryptdef.cli.core.process_file")
@patch("encryptdef.cli.assigning_a_name_file", return_value="decrypt-test.txt")
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
    """Teste para o comando decrypt com um arquivo e keyfile"""

    result = runner.invoke(
        main, ["decrypt", "--keyfile", "key.txt", "--file", "encrypt-test.txt"]
    )
    assert result.exit_code == 0
    mock_process_keyfile.assert_called_once_with(
        "key.txt", None, "encrypt-test.txt", TEMPLATE_DECRYPT_KEY
    )
    mock_assigning.assert_called_once_with("encrypt-test.txt", "decrypt-")
    mock_process_file.assert_called_once_with(
        ["encrypt-test.txt", "mock_key_file", "decrypt-test.txt"], core.decrypt
    )
