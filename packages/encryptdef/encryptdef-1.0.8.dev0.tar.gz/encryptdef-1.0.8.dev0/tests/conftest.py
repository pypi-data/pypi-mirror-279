"""Módulo de configurações dos testes"""

import pytest


@pytest.fixture(autouse=True)
def go_to_tmpdir(request):  # injeção de dependencias
    """Cada teste tem um diretorio no /tmp"""
    tmpdir = request.getfixturevalue("tmpdir")
    with tmpdir.as_cwd():
        yield  # protocolo de generators
