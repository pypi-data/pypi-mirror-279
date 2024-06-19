"""Módulo que contém as funções principais da ferramenta"""

import hashlib
import sys
from base64 import b64decode, b64encode
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Optional, Union

import rich_click as click
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from rich.progress import Progress

from encryptdef.interactive_interface import (
    print_continue_or_leave,
    print_get_max_workers,
    print_request_menu,
    print_requesting_file,
    print_requesting_message,
    print_success_message,
)
from encryptdef.log import print_and_record_log
from encryptdef.settings import CURRENT_DIR, console
from encryptdef.template import (
    TEMPLATE_CONTINUE_LEAVE,
    TEMPLATE_DECRYPT_FILE,
    TEMPLATE_DECRYPT_KEY,
    TEMPLATE_DECRYPT_MESSAGE,
    TEMPLATE_DECRYPTED,
    TEMPLATE_DECRYPTED_FILE,
    TEMPLATE_DECRYPTED_MESSAGE,
    TEMPLATE_EMPTY_FILE_ERROR,
    TEMPLATE_ENCRYPT_FILE,
    TEMPLATE_ENCRYPT_KEY,
    TEMPLATE_ENCRYPT_MESSAGE,
    TEMPLATE_ENCRYPTED,
    TEMPLATE_ENCRYPTED_FILE,
    TEMPLATE_ENCRYPTED_MESSAGE,
    TEMPLATE_ERROR_EMPTY_FIELD,
    TEMPLATE_ERROR_INVALID_ENCRYPTED_FORMAT,
    TEMPLATE_FILE_NOT_FOUND,
    TEMPLATE_INFO_FILE,
    TEMPLATE_INVALID_KEY,
    TEMPLATE_MENU_ENCRYPT_DECRYPT,
    TEMPLATE_MENU_MESSAGE_FILE,
    TEMPLATE_TASK_DESCRIPTION,
    TEMPLATE_TYPE_ERROR,
)
from encryptdef.utils import get_new_file_path, read_file, write_file


class InvalidEncryptedFormat(Exception):
    """Formato de string criptografada inválido"""


class InvalidKey(Exception):
    """Formato de string criptografada inválido"""


class EmptyFileError(Exception):
    """Formato de string criptografada inválido"""


def encrypt(message: str, password: str) -> str:
    """
    Criptografa uma mensagem usando AES GCM com uma chave derivada por Scrypt.

    Args:
        message (str): A mensagem que será criptografada.
        password (str): A senha usada para derivar a chave de criptografia.

    Returns:
        str: A mensagem criptografada contendo texto cifrado, salt,
        nonce e tag.
    """
    # Gera um salt aleatório
    salt = get_random_bytes(AES.block_size)

    # Usa Scrypt para derivar a chave privada a partir da senha
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32
    )

    # Cria a configuração do cifrador em modo GCM
    cipher = AES.new(private_key, AES.MODE_GCM)
    cipher_text, tag = cipher.encrypt_and_digest(message.encode("utf-8"))

    # Codifica em base64 e retorna uma string formatada
    encrypted_parts = {
        "cipher_text": b64encode(cipher_text).decode("utf-8"),
        "salt": b64encode(salt).decode("utf-8"),
        "nonce": b64encode(cipher.nonce).decode("utf-8"),
        "tag": b64encode(tag).decode("utf-8"),
    }

    return "*".join(encrypted_parts.values())


def decrypt(enc_string: str, password: str) -> str:
    """
    Descriptografa uma mensagem criptografada usando AES GCM com uma chave
    derivada por Scrypt.

    Args:
        enc_string (str): A mensagem criptografada.
        password (str): A senha usada para derivar a chave de descriptografia.

    Returns:
        str: A mensagem descriptografada ou uma mensagem de erro.
    """
    try:
        enc_parts = enc_string.split("*")
        if len(enc_parts) != 4:
            raise InvalidEncryptedFormat(
                TEMPLATE_ERROR_INVALID_ENCRYPTED_FORMAT
            )

        # Decodifica as partes criptografadas de base64
        cipher_text, salt, nonce, tag = map(b64decode, enc_parts)

        # Gera a chave privada a partir da senha e do salt
        private_key = hashlib.scrypt(
            password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32
        )

        # Cria a configuração do cifrador em modo GCM
        cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

        # Descriptografa o texto cifrado e verifica a tag
        decrypted = cipher.decrypt_and_verify(cipher_text, tag)

        return decrypted.decode("utf-8")

    except ValueError as e:
        raise InvalidKey(TEMPLATE_INVALID_KEY) from e


def encrypt_message(message: str, key: str) -> None:
    """
    Criptografa os dados usando a chave fornecida e exibe o resultado.

    Args:
        message (str): Dados a serem criptografados.
        key (str): Chave para criptografia.
    """
    encrypted_message = encrypt(message, key)
    print_success_message(
        encrypted_message, TEMPLATE_ENCRYPTED_MESSAGE, TEMPLATE_ENCRYPTED
    )


def decrypt_message(message: str, key: str) -> bool:
    """
    Descriptografa os dados usando a chave fornecida. Se a descriptografia
    falhar, retorna False; caso contrário, exibe o resultado e retorna True.

    Args:
        message (str): Dados a serem descriptografados.
        key (str): Chave para descriptografia.

    Returns:
        bool: True se a descriptografia for bem-sucedida, False caso contrário.
    """
    try:
        decrypted_message = decrypt(message, key)

        if isinstance(decrypted_message, str):
            print_success_message(
                decrypted_message,
                TEMPLATE_DECRYPTED_MESSAGE,
                TEMPLATE_DECRYPTED,
            )
            return True

    except (InvalidEncryptedFormat, InvalidKey) as e:
        print_and_record_log(str(e), "error")
    return False


def process_lines(
    lines: List[str],
    key: str,
    process_line_func: Callable[[str, str], Union[str, bool]],
    max_workers: int,
) -> List[str]:
    """
    Processa cada linha do arquivo usando a função fornecida.

    Args:
        lines (List[str]): Lista de linhas do arquivo.
        key (str): Chave para criptografar ou descriptografar.
        process_line_func (Callable[[str, str], Union[str, bool]]): Função para
        processar cada linha.
        max_workers (int): Número máximo de núcleos da CPU a serem usados.

    Returns:
        List[str]: Lista de linhas processadas.
    """
    indexed_processed_lines = []

    with Progress() as progress:
        task = progress.add_task(TEMPLATE_TASK_DESCRIPTION, total=len(lines))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submete as linhas para processamento junto com seus índices
            future_to_index = {
                executor.submit(
                    process_line_func, line.rstrip("\n"), key
                ): index
                for index, line in enumerate(lines)
            }

            for future in as_completed(future_to_index):
                result = future.result()

                if not isinstance(result, str):
                    raise TypeError(TEMPLATE_TYPE_ERROR % {type(result)})

                # Adiciona o resultado junto com o índice original
                indexed_processed_lines.append(
                    (future_to_index[future], result)
                )

                # Atualiza a barra de progresso
                progress.update(task, advance=1)

    # Ordena os resultados processados pela ordem original das linhas
    indexed_processed_lines.sort(key=lambda x: x[0])

    # Retorna apenas as linhas processadas, na ordem correta
    return [line + "\n" for index, line in indexed_processed_lines]


def process_file_content(
    file_path: str,
    key: str,
    new_file_path: str,
    process_line_func: Callable[[str, str], Union[str, bool]],
) -> bool:
    """
    Processa o conteúdo de um arquivo e salva o resultado em um novo arquivo.

    Args:
        file_path (str): Caminho do arquivo original.
        key (str): Chave para criptografar ou descriptografar.
        new_file_path (str): Caminho do novo arquivo.
        process_line_func (Callable[[str, str], Union[str, bool]]): Função para
        processar cada linha.

    Returns:
        bool: True se o processamento for bem-sucedido, False caso contrário.
    """
    lines = read_file(file_path)
    if not lines:
        raise EmptyFileError(TEMPLATE_EMPTY_FILE_ERROR % file_path)

    max_workers = print_get_max_workers(lines)
    processed_lines = process_lines(lines, key, process_line_func, max_workers)

    write_file(new_file_path, processed_lines)
    print_and_record_log(
        (
            TEMPLATE_ENCRYPTED_FILE % new_file_path
            if process_line_func is encrypt
            else TEMPLATE_DECRYPTED_FILE % new_file_path
        ),
        "debug",
    )

    return True


def process_file(
    data_list: List[str],
    process_line_func: Callable[[str, str], Union[str, bool]],
) -> bool:
    """
    Processa o conteúdo de um arquivo linha por linha usando a função fornecida
    e salva o resultado em um novo arquivo.

    Args:
        data_list (List[str]): Lista contendo [arquivo, chave, novo_arquivo].
        process_line_func (Callable[[str, str], Union[str, bool]]): Função para
        processar cada linha do arquivo.

    Returns:
        bool: True se o processamento for bem-sucedido, False caso contrário.
    """
    try:
        file_path, key, new_file = data_list
        new_file_path = get_new_file_path(file_path, new_file, CURRENT_DIR)
        return process_file_content(
            file_path, key, new_file_path, process_line_func
        )

    except FileNotFoundError:
        print_and_record_log(TEMPLATE_FILE_NOT_FOUND % file_path, "error")
        console.print(TEMPLATE_INFO_FILE)
        return False

    except (
        TypeError,
        IsADirectoryError,
        ValueError,
        InvalidEncryptedFormat,
        InvalidKey,
        EmptyFileError,
    ) as e:
        print_and_record_log(str(e), "error")
        return False


def process_keyfile_and_args(
    keyfile: Optional[str],
    message: Optional[str],
    file_: Optional[str],
    template_key: str,
) -> str:
    """
    Obtém a chave de criptografia e valida os argumentos.

    Processa a chave de criptografia a partir de um arquivo ou solicita ao
    usuário, e valida se 'message' ou 'file' foram fornecidos corretamente.

    Args:
        keyfile (Optional[str]): Caminho para o arquivo com a chave. Se None,
        a chave será solicitada.
        message (Optional[str]): Dados para criptografar ou descriptografar.
        Usado se 'file' não for fornecido.
        file_ (Optional[str]): Caminho do arquivo a ser criptografado ou
        descriptografado. Usado se 'message' não for fornecido.
        template_key (str): Template para solicitar a chave ao usuário,
        se necessário.

    Returns:
        str: A chave de criptografia obtida.

    Raises:
        click.UsageError: Se ambos ou nenhum dos argumentos 'message' e 'file'
        forem fornecidos.
        SystemExit: Se o arquivo de chave não for encontrado, ou se a chave
        fornecida for inválida.
    """
    if message and file_:
        raise click.UsageError(
            "Você deve fornecer apenas um dos argumentos: --message ou --file,"
            " não ambos."
        )
    if not message and not file_:
        raise click.UsageError(
            "Você deve fornecer um dos argumentos: --message ou --file."
        )

    key: Optional[str] = None
    if keyfile:
        try:
            key = "".join(read_file(keyfile)).strip()
        except FileNotFoundError:
            print_and_record_log(TEMPLATE_FILE_NOT_FOUND % keyfile, "error")
            sys.exit(1)
    else:
        while not key or key.isspace():
            key = console.input(template_key, password=True).strip()
            if not key:
                print_and_record_log(TEMPLATE_ERROR_EMPTY_FIELD, "error")

    return key


def interactive_mode() -> None:
    """
    Função principal do modo interativo que chama outras funções.
    """
    while True:
        file_message_option = print_request_menu(TEMPLATE_MENU_MESSAGE_FILE)

        match file_message_option:
            case 1:
                message_encrypt_decrypt_option = print_request_menu(
                    TEMPLATE_MENU_ENCRYPT_DECRYPT
                )

                match message_encrypt_decrypt_option:
                    case 1:
                        message, key = print_requesting_message(
                            TEMPLATE_ENCRYPT_MESSAGE, TEMPLATE_ENCRYPT_KEY
                        )
                        encrypt_message(message, key)
                    case 2:
                        message, key = print_requesting_message(
                            TEMPLATE_DECRYPT_MESSAGE, TEMPLATE_DECRYPT_KEY
                        )
                        decrypt_message(message, key)

            case 2:
                file_encrypt_decrypt_option = print_request_menu(
                    TEMPLATE_MENU_ENCRYPT_DECRYPT
                )
                match file_encrypt_decrypt_option:
                    case 1:
                        file_list = print_requesting_file(
                            TEMPLATE_ENCRYPT_FILE
                        )
                        process_file(file_list, encrypt)
                    case 2:
                        file_list = print_requesting_file(
                            TEMPLATE_DECRYPT_FILE
                        )
                        process_file(file_list, decrypt)

        if print_continue_or_leave(TEMPLATE_CONTINUE_LEAVE):
            break
