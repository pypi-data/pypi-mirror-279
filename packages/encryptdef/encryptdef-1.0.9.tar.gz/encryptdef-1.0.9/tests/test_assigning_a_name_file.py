""" Modulo para testar a função assigning_a_name_file em utils.py"""

from encryptdef.utils import assigning_a_name_file


def test_assigning_a_name_file_absolute():
    """Testando a função assigning_a_name_file"""
    file = "/tmp/test/file-test-123.txt"
    name = "encrypt-"
    expected_result = "/tmp/test/encrypt-file-test-123.txt"

    result = assigning_a_name_file(file, name)
    assert result == expected_result


def test_assigning_a_name_file_relative():
    """Testando a função assigning_a_name_file"""
    file = "-123-file-test.txt"
    name = "decrypt-"
    expected_result = "decrypt--123-file-test.txt"

    result = assigning_a_name_file(file, name)
    assert result == expected_result
