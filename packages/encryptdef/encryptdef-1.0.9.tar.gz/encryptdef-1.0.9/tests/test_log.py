""" Modulo para testar  log.py"""

import logging
import os
from logging import handlers
from unittest.mock import patch

from encryptdef.log import configure_logger, get_logger, print_and_record_log


def clear_logger_handlers():
    """Função para limpar as configurações do log"""
    logger = get_logger()
    logger.handlers.clear()  # Limpa todos os handlers
    logger.setLevel(logging.NOTSET)  # Redefine o nível do logger
    # Garante que o logger não propague para loggers de nível superior
    logger.propagate = False
    logging.basicConfig(
        level=logging.NOTSET
    )  # Redefine a configuração básica do logging


def create_log_file():
    """Criando um arquivo de log no diretorio atual"""
    clear_logger_handlers()
    current_dir = os.getcwd()
    logfile = os.path.join(current_dir, "encryptdef.log")
    configure_logger("WARNING", logfile)

    return logfile


def test_configure_logger_creates_logfile():
    """Testando as configurações de log"""
    logfile = create_log_file()
    logger = get_logger()

    assert any(
        isinstance(handler, handlers.RotatingFileHandler)
        for handler in logger.handlers
    )
    assert logger.level == logging.WARNING
    assert os.path.isfile(logfile)


def test_get_logger():
    """Testando a função get_looger"""
    clear_logger_handlers()
    logger = get_logger()
    assert logger is not None
    assert isinstance(logger, logging.Logger)
    assert logger.name == "encryptdef"


def test_print_and_record_log_info():
    """Testando o conteudo do arquivo log em modo info"""
    clear_logger_handlers()
    current_dir = os.getcwd()
    logfile = os.path.join(current_dir, "encryptdef.log")
    configure_logger("INFO", logfile)
    get_logger()

    with patch("encryptdef.settings.console.print") as mock_console_print:
        print_and_record_log("Info message")
        mock_console_print.assert_called_once_with(
            "Info message", style="info"
        )

    with open(logfile, "r", encoding="utf-8") as log_file:
        log_contents = log_file.read()
        assert "Info message" in log_contents


def test_print_and_record_log_warning():
    """Testando o conteudo do arquivo log em modo warning"""
    clear_logger_handlers()
    logfile = create_log_file()
    get_logger()

    with patch("encryptdef.settings.console.print") as mock_console_print:
        print_and_record_log("Info message", "warning")
        mock_console_print.assert_called_once_with(
            "Info message", style="warning"
        )

    with open(logfile, "r", encoding="utf-8") as log_file:
        log_contents = log_file.read()
        assert "Info message" in log_contents


def test_configure_logger_creates_logfile_root_dir(monkeypatch):
    """Testando as configurações de log"""
    clear_logger_handlers()
    current_dir = os.getcwd()
    logfile = os.path.join(current_dir, "encryptdef.log")
    monkeypatch.setattr("encryptdef.log.__file__", logfile)

    configure_logger("WARNING")
    logger = get_logger()

    assert any(
        isinstance(handler, handlers.RotatingFileHandler)
        for handler in logger.handlers
    )
    assert logger.level == logging.WARNING
    assert os.path.isfile(logfile)
