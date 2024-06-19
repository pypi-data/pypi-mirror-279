"""Módulo que contém as funções principais da ferramenta"""

import os
import re
from typing import List

from encryptdef.template import TEMPLATE_IS_DIRECTORY


def get_new_file_path(file: str, new_file: str, current_dir: str) -> str:
    """
    Retorna o caminho completo do novo arquivo e valida se não é um diretório.

    Args:
        file (str): Caminho do arquivo original.
        new_file (str): Nome do novo arquivo.
        current_dir (str): Caminho do diretório atual.

    Returns:
        str: Caminho completo do novo arquivo.

    Raises:
        IsADirectoryError: Se algum dos caminhos fornecidos for um diretório.
    """
    if not os.path.isabs(file):
        new_file_path = os.path.join(current_dir, new_file)
    else:
        new_file_path = new_file

    new_file_path = os.path.normpath(new_file_path)  # Normaliza o caminho

    for path in [file, new_file_path]:
        if os.path.isdir(path):
            raise IsADirectoryError(TEMPLATE_IS_DIRECTORY % path)

    return new_file_path


def assigning_a_name_file(file: str, name: str) -> str:
    """
    Retorna o novo nome de arquivo com o prefixo fornecido, removendo quaisquer
    padrões de criptografia/descriptografia do nome original.

    Args:
        file (str): Caminho do arquivo original.
        name (str): Prefixo para o novo nome do arquivo.

    Returns:
        str: Novo caminho do arquivo.
    """

    def _get_new_name(filename: str) -> str:
        return name + re.sub(r"encrypt-|decrypt-", "", filename)

    if os.path.isabs(file):
        filename = os.path.basename(file)
        new_file_path = _get_new_name(filename)
        return os.path.join(os.path.dirname(file), new_file_path)

    new_file = _get_new_name(file)
    return os.path.normpath(new_file)  # Normaliza o caminho


def read_file(file: str) -> List[str]:
    """
    Lê o conteúdo do arquivo e retorna uma lista de linhas.

    Args:
        file (str): Caminho do arquivo a ser lido.

    Returns:
        List[str]: Lista de linhas do arquivo.
    """
    with open(file, "r", encoding="utf-8", errors="ignore") as file_:
        return file_.readlines()


def write_file(new_file_path: str, processed_lines: List[str]) -> None:
    """
    Escreve as linhas processadas em um novo arquivo.

    Args:
        new_file_path (str): Caminho do novo arquivo.
        processed_lines (List[str]): Lista de linhas processadas.
    """
    with open(new_file_path, "w", encoding="utf-8") as file_a:
        file_a.writelines(processed_lines)


def clear_console():
    """Limpa o console de forma segura.
    Utilizando sequências de escape ANSI"""
    if os.name == "posix":
        print("\033[H\033[J", end="")
    elif os.name == "nt":
        print("\033c", end="")
