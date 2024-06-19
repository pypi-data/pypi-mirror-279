""" Modulo para testar a função get_new_file_path em utils.py"""

import os

import pytest

from encryptdef.utils import get_new_file_path


def test_get_new_file_path_positive():
    """Testando a função get_new_file_path"""
    current_dir = os.getcwd()
    file = "file_test.txt"
    new_file = "encrypt_file_test.txt"
    expected_path = os.path.join(current_dir, new_file)

    file_path = get_new_file_path(file, new_file, current_dir)
    assert file_path == expected_path


def test_get_new_file_path_is_directory_error():
    """Testando a função get_new_file_path"""
    current_dir = os.getcwd()
    directoty = "new_directory"
    directoty_path = os.path.join(current_dir, directoty)
    os.mkdir(directoty_path)

    with pytest.raises(IsADirectoryError):
        get_new_file_path(directoty_path, "new_test.txt", current_dir)

    with pytest.raises(IsADirectoryError):
        get_new_file_path("test.txt", directoty_path, current_dir)


def test_get_new_file_path_positive_exact_file_path():
    """Testando a função get_new_file_path"""
    file = "file_test.txt"
    new_file = "encrypt_file_test.txt"

    current_dir = os.getcwd()
    new_file_path = os.path.join(current_dir, new_file)

    new_file_path_get = get_new_file_path(file, new_file_path, current_dir)
    assert new_file_path_get == new_file_path
