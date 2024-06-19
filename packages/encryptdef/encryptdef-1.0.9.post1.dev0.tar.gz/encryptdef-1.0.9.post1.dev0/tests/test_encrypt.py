"""Modulo para testar a função encrypt em core.py"""

import base64

import pytest

from encryptdef.core import encrypt


def test_encrypt_output_format():
    """Testa a função encrypt"""
    message = "This is a test message."
    password = "strongpassword123"

    encrypted_message = encrypt(message, password)

    # Verificar se a mensagem criptografada contém 4 partes separadas por '*'
    parts = encrypted_message.split("*")
    assert (
        len(parts) == 4
    ), "Encrypted message should contain 4 parts separated by '*'"

    # Verificar se cada parte pode ser decodificada de base64
    cipher_text, salt, nonce, tag = parts
    try:
        base64.b64decode(cipher_text)
        base64.b64decode(salt)
        base64.b64decode(nonce)
        base64.b64decode(tag)
    except TypeError:
        pytest.fail("One of the parts could not be base64 decoded")


def test_encrypt_different_messages():
    """Testa a função encrypt diferentes valores e mesma senha"""
    password = "strongpassword123"
    message1 = "Message one"
    message2 = "Message two"

    encrypted_message1 = encrypt(message1, password)
    encrypted_message2 = encrypt(message2, password)

    assert encrypted_message1 != encrypted_message2


def test_encrypt_same_message_different_passwords():
    """Testa a função encrypt diferentes senhas e mesmo valor"""
    message = "This is a test message."
    password1 = "password123"
    password2 = "differentpassword456"

    encrypted_message1 = encrypt(message, password1)
    encrypted_message2 = encrypt(message, password2)

    assert encrypted_message1 != encrypted_message2
