""" Modulo para testar a função read_file em utils.py"""

import os
from random import randint, sample
from string import ascii_letters, digits

from encryptdef.utils import read_file


def teste_read_file_positive():
    """Testando a função read_file"""
    file_name = "filte_test.txt"
    file_content = [
        "".join(sample(ascii_letters + digits, randint(1, 62))) + "\n"
        for number in range(0, 500)
    ]

    current_dir = os.getcwd()
    file = os.path.join(current_dir, file_name)
    with open(file, "w", encoding="utf-8") as file_:
        file_.writelines(file_content)

    read_file_test = read_file(file)

    assert read_file_test == file_content
