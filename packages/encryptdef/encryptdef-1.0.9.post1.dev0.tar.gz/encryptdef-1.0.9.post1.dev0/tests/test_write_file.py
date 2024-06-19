""" Modulo para testar a função write_file em utils.py"""

import os
from random import randint, sample
from string import ascii_letters, digits

from encryptdef.utils import write_file


def teste_write_file_positive():
    """Testando a função write_file"""
    file_name = "filte_test.txt"
    file_content = [
        "".join(sample(ascii_letters + digits, randint(1, 62))) + "\n"
        for number in range(0, 500)
    ]

    current_dir = os.getcwd()
    file = os.path.join(current_dir, file_name)
    write_file(file, file_content)

    with open(file, "r", encoding="utf-8") as file_:
        file_content_read = file_.readlines()

    assert file_content_read == file_content
