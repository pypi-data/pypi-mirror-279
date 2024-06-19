"""Modulo para testar a função process_file_content em core.py"""

from unittest.mock import patch

import pytest
import rich_click as click

from encryptdef.core import process_keyfile_and_args
from encryptdef.template import TEMPLATE_FILE_NOT_FOUND


def test_process_keyfile_and_args_both_message_and_file_error():
    """Testa a função process_keyfile_and_args"""
    click_error = (
        "Você deve fornecer apenas um dos argumentos: --message ou --file,"
        " não ambos."
    )
    with pytest.raises(click.UsageError) as error:
        process_keyfile_and_args("keyfile", "message", "file", "template_key")

    assert str(error.value) == click_error


def test_process_keyfile_and_args_neither_message_nor_file_error():
    """Testa a função process_keyfile_and_args"""
    click_error = "Você deve fornecer um dos argumentos: --message ou --file."
    with pytest.raises(click.UsageError) as error:
        process_keyfile_and_args("keyfile", None, None, "template_key")

    assert str(error.value) == click_error


def test_process_keyfile_and_args_keyfile_not_found():
    """Testa a função process_keyfile_and_args"""
    with (
        patch("encryptdef.core.print_and_record_log") as mock_log,
        patch("encryptdef.core.read_file", side_effect=FileNotFoundError),
    ):
        with pytest.raises(SystemExit):
            process_keyfile_and_args(
                "non_existent_keyfile", None, "file", "template_key"
            )

        mock_log.assert_called_with(
            TEMPLATE_FILE_NOT_FOUND % "non_existent_keyfile", "error"
        )


def test_process_keyfile_and_args_keyfile_success():
    """Testa a função process_keyfile_and_args"""
    with patch("encryptdef.core.read_file", return_value=["test_key"]):
        key = process_keyfile_and_args("keyfile", None, "file", "template_key")
        assert key == "test_key"
