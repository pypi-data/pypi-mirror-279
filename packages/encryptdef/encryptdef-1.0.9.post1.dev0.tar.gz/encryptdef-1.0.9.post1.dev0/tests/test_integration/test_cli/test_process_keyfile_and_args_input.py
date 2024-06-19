""" Modulo para testar a função process_keyfile_and_args em core.py"""

from unittest.mock import patch

from encryptdef.core import process_keyfile_and_args
from encryptdef.template import TEMPLATE_ERROR_EMPTY_FIELD


def test_process_keyfile_and_args_input_key_success(monkeypatch):
    """Testa a função process_keyfile_and_args"""
    # Define a chave de entrada que será retornada pelo mock
    test_key = "test_key"

    # Usa monkeypatch para substituir console.input para sempre retornar
    # 'test_key'
    # A função lambda aceita quaisquer argumentos posicionais (*args)
    # e quaisquer argumentos nomeados (**kwargs) que possam ser passados para
    # console.input
    monkeypatch.setattr(
        "encryptdef.core.console.input", lambda *args, **kwargs: test_key
    )

    # Chama a função com os argumentos apropriados e verifica se a chave
    # retornada é 'test_key'
    key = process_keyfile_and_args(None, "message", None, "template_key")
    assert key == test_key


def test_process_keyfile_and_args_key_isspace():
    """Testa a função process_keyfile_and_args"""
    with (
        patch("encryptdef.core.read_file", return_value=[]),
        patch(
            "encryptdef.core.console.input", side_effect=["   ", "valid_key"]
        ),
        patch("encryptdef.core.print_and_record_log") as mock_log,
    ):

        process_keyfile_and_args(
            keyfile=None,
            message="fake_message",
            file_=None,
            template_key="Enter key",
        )

        mock_log.assert_called_with(TEMPLATE_ERROR_EMPTY_FIELD, "error")
