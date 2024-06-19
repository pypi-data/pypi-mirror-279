"""Módulo responsável por todos os comandos CLI"""

from importlib.metadata import version
from typing import List, Optional

import rich_click as click

from encryptdef import core
from encryptdef.template import TEMPLATE_DECRYPT_KEY, TEMPLATE_ENCRYPT_KEY
from encryptdef.utils import assigning_a_name_file

# Configurações do Rich Click
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.USE_MARKDOWN = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.SHOW_METAVARS_COLUMN = False
click.rich_click.APPEND_METAVARS_HELP = True


@click.group(invoke_without_command=True)
@click.version_option(version("encryptdef"))
@click.pass_context
def main(ctx: Optional[click.Context] = None) -> None:
    """Encryptdef

    Ferramenta de linha de comando em Python para encriptar e desencriptar
    dados e arquivos de forma segura.

    **Principais Funcionalidades:**
    - Encriptação e desencriptação de dados e arquivos.
    - Utilização de uma chave de criptografia fornecida pelo usuário.

    **Como Funciona:**
    Encryptdef utiliza criptografia AES GCM (Galois/Counter Mode) com chave
    derivada pelo algoritmo Scrypt, garantindo uma proteção robusta para
    seus dados.

    **Nota Importante:**
    > **Mantenha a chave de encriptação em segredo e não a perca. Sem a chave
    correta, não será possível desencriptar os dados ou arquivos.**
    """
    if ctx is None:
        ctx = click.Context(main)  # pragma: no cover

    if ctx.invoked_subcommand is None:
        core.interactive_mode()


@main.command()
@click.option(
    "--keyfile",
    required=False,
    help="Caminho para o arquivo contendo a chave de encriptação.",
)
@click.option("--message", required=False, help="Dados para encriptar.")
@click.option("--file", required=False, help="Arquivo para encriptar.")
def encrypt(
    keyfile: Optional[str],
    message: Optional[str],
    file: Optional[str],
) -> None:
    """
    Encriptar dados e arquivos.

    Args:
        keyfile (Optional[str]): Caminho para o arquivo contendo a chave de
        encriptação.
        message (Optional[str]): Dados para encriptar.
        file (Optional[str]): Arquivo para encriptar.
    """
    key = core.process_keyfile_and_args(
        keyfile, message, file, TEMPLATE_ENCRYPT_KEY
    )

    if message:
        core.encrypt_message(message, key)

    elif file:
        new_file = assigning_a_name_file(file, "encrypt-")
        data_list: List[str] = [file, key, new_file]
        core.process_file(data_list, core.encrypt)


@main.command()
@click.option(
    "--keyfile",
    required=False,
    help="Caminho para o arquivo contendo a chave de decriptação.",
)
@click.option("--message", required=False, help="Dados para decriptar.")
@click.option("--file", required=False, help="Arquivo para decriptar.")
def decrypt(
    keyfile: Optional[str],
    message: Optional[str],
    file: Optional[str],
) -> None:
    """
    Decriptar dados e arquivos.

    Args:
        keyfile (Optional[str]): Caminho para o arquivo contendo a chave de
        decriptação.
        message (Optional[str]): Dados para decriptar.
        file (Optional[str]): Arquivo para decriptar.
    """
    key = core.process_keyfile_and_args(
        keyfile, message, file, TEMPLATE_DECRYPT_KEY
    )

    if message:
        core.decrypt_message(message, key)

    elif file:
        new_file = assigning_a_name_file(file, "decrypt-")
        data_list: List[str] = [file, key, new_file]
        core.process_file(data_list, core.decrypt)
