"""Módulo que contém as configurações do logging"""

import logging
import os
from logging import handlers
from typing import Optional, Union

from encryptdef.settings import console

LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()

log_instance = logging.getLogger("encryptdef")  # Criando instância de log

# Objeto de formatação de como serão exibidos os logs
fmt = logging.Formatter(
    "%(asctime)s %(name)s %(levelname)s "
    "l:%(lineno)d f:%(filename)s: %(message)s"
)


def configure_logger(
    log_level: str, logfile: Optional[Union[str, os.PathLike[str]]] = None
) -> None:
    """Configura o logger com um handler de arquivo rotativo."""
    if logfile is None:
        # Obtém o diretório raiz do programa
        root_dir = os.path.dirname(os.path.abspath(__file__))
        logfile = os.path.join(root_dir, "encryptdef.log")

    # Verifica se o logger já possui handlers para evitar duplicações
    if not log_instance.hasHandlers():
        fh = handlers.RotatingFileHandler(
            logfile, maxBytes=10**6, backupCount=10
        )
        fh.setLevel(log_level)
        fh.setFormatter(fmt)
        log_instance.addHandler(fh)
        log_instance.setLevel(log_level)


def get_logger() -> logging.Logger:
    """Retorna o logger configurado."""
    return log_instance


# Configure o logger ao importar o módulo
configure_logger(LOG_LEVEL)

log = get_logger()


def print_and_record_log(msg: str, style: Optional[str] = None) -> None:
    """
    Loga uma mensagem e a imprime no console com um estilo especificado.

    Args:
        msg (str): A mensagem a ser logada e impressa.
        style (Optional[str]): O estilo da mensagem de log. Valores possíveis
        são "critical", "error", "warning", "info" e "debug".
        Padrão é None.

    Returns:
        None
    """
    # Garantir que a chave seja sempre uma string
    if style is None:
        style = "info"

    log_func = {
        "critical": log.critical,
        "error": log.error,
        "warning": log.warning,
        "info": log.info,
        "debug": log.debug,
    }.get(
        style, log.info
    )  # Garantir que sempre retornará uma função

    log_func(msg.strip())
    console.print(msg, style=style)
