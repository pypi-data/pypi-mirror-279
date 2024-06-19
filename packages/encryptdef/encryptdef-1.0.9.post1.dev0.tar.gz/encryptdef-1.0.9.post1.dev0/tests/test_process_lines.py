"""Modulo para testar a função process_lines em core.py"""

import pytest

from encryptdef.core import decrypt, encrypt, process_lines


# Funções de exemplo para processamento de linha
def mock_process_line_func(line, key):
    """Função exemplo process_line"""
    return f"processed_{line}_with_{key}"


def mock_process_line_func_invalid(line, key):  # pylint: disable=W0613
    """Função exemplo de retorno invalido"""
    return 123  # Deve ser string, mas retorna int para simular erro


def mock_process_line_func_exception(line, key):
    """Função exemplo de expection"""
    raise ValueError("Simulated processing error")


def test_process_lines_basic():
    """Testa a função process_lines"""
    lines = ["line1", "line2", "line3"]
    key = "testkey"
    max_workers = 2
    processed_lines = process_lines(
        lines, key, mock_process_line_func, max_workers
    )
    expected = [
        "processed_line1_with_testkey\n",
        "processed_line2_with_testkey\n",
        "processed_line3_with_testkey\n",
    ]
    assert processed_lines == expected


def test_process_lines_empty():
    """Testa a função process_lines"""
    lines = []
    key = "testkey"
    max_workers = 2
    processed_lines = process_lines(
        lines, key, mock_process_line_func, max_workers
    )
    assert processed_lines == []


def test_process_lines_single_worker():
    """Testa a função process_lines"""
    lines = ["line1"]
    key = "testkey"
    max_workers = 1
    processed_lines = process_lines(
        lines, key, mock_process_line_func, max_workers
    )
    expected = ["processed_line1_with_testkey\n"]
    assert processed_lines == expected


def test_process_lines_multiple_workers():
    """Testa a função process_lines"""
    lines = ["line1", "line2", "line3"]
    key = "testkey"
    max_workers = 3
    processed_lines = process_lines(
        lines, key, mock_process_line_func, max_workers
    )
    expected = [
        "processed_line1_with_testkey\n",
        "processed_line2_with_testkey\n",
        "processed_line3_with_testkey\n",
    ]
    assert processed_lines == expected


def test_process_lines_order_preserved():
    """Testa a função process_lines"""
    lines = ["line1", "line2", "line3"]
    key = "testkey"
    max_workers = 2
    processed_lines = process_lines(
        lines, key, mock_process_line_func, max_workers
    )
    expected = [
        "processed_line1_with_testkey\n",
        "processed_line2_with_testkey\n",
        "processed_line3_with_testkey\n",
    ]
    assert processed_lines == expected


def test_process_lines_invalid_return_type():
    """Testa a função process_lines"""
    lines = ["line1"]
    key = "testkey"
    max_workers = 1
    with pytest.raises(TypeError):
        process_lines(lines, key, mock_process_line_func_invalid, max_workers)


def test_process_lines_processing_exception():
    """Testa a função process_lines"""
    lines = ["line1"]
    key = "testkey"
    max_workers = 1
    with pytest.raises(ValueError, match="Simulated processing error"):
        process_lines(
            lines, key, mock_process_line_func_exception, max_workers
        )


def test_process_lines_with_encryption():
    """Testa a função process_lines"""
    lines = ["hello", "world"]
    key = "password"
    max_workers = 2
    processed_lines = process_lines(lines, key, encrypt, max_workers)

    # Verifica se ambas as linhas foram processadas
    assert len(processed_lines) == 2

    # Verifica se todas as linhas são strings
    assert all(isinstance(line, str) for line in processed_lines)


def test_process_lines_with_decryption():
    """Testa a função process_lines"""
    encrypted_lines = [
        encrypt("hello", "password"),
        encrypt("world", "password"),
    ]
    key = "password"
    max_workers = 2
    processed_lines = process_lines(encrypted_lines, key, decrypt, max_workers)
    expected = ["hello\n", "world\n"]
    assert processed_lines == expected
