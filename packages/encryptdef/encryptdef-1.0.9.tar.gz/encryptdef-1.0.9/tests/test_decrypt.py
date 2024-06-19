"""Modulo para testar a função decrypt em core.py"""

from base64 import b64decode, b64encode

import pytest

from encryptdef.core import (
    InvalidEncryptedFormat,
    InvalidKey,
    decrypt,
    encrypt,
)
from encryptdef.template import (
    TEMPLATE_ERROR_INVALID_ENCRYPTED_FORMAT,
    TEMPLATE_INVALID_KEY,
)


def test_decrypt_correct_message():
    """Testa a função decrypt"""
    message1 = "Message one: djas;kl/d<j@!#@'>$!@&()&&¨|#!@&*%#312312adasd"
    password1 = "strongpassword123"

    message2 = "Message two: 1~[]31'2>~[]dADd12<asS&(*¨*&¨#%@!#!@/HDJKA@!#"
    password2 = "djas;kl/d<j@!#@'>$!@&()&&¨|#!@&*%#312312adasd"

    encrypted_message1 = encrypt(message1, password1)
    decrypted_message1 = decrypt(encrypted_message1, password1)

    encrypted_message2 = encrypt(message2, password2)
    decrypted_message2 = decrypt(encrypted_message2, password2)

    assert decrypted_message1 == message1
    assert decrypted_message2 == message2


def test_decrypt_with_wrong_password():
    """Testa a função decrypt"""
    message = "This is a test message."
    password = "strongpassword123"
    wrong_password = "wrongpassword456"

    encrypted_message = encrypt(message, password)

    with pytest.raises(InvalidKey) as excinfo:
        decrypt(encrypted_message, wrong_password)
    assert str(excinfo.value) == TEMPLATE_INVALID_KEY


def test_decrypt_invalid_format():
    """Testa a função decrypt"""
    invalid_encrypted_message = "invalid*encrypted*message-format"
    password = "strongpassword123"

    with pytest.raises(InvalidEncryptedFormat) as excinfo:
        decrypt(invalid_encrypted_message, password)

    assert str(excinfo.value) == TEMPLATE_ERROR_INVALID_ENCRYPTED_FORMAT


def test_decrypt_with_modified_message():
    """Testa a função decrypt"""
    message = "This is a test message."
    password = "strongpassword123"

    encrypted_message = encrypt(message, password)
    parts = encrypted_message.split("*")
    modified_cipher_text = b64encode(b"modified" + b64decode(parts[0])).decode(
        "utf-8"
    )
    modified_encrypted_message = "*".join([modified_cipher_text] + parts[1:])

    with pytest.raises(InvalidKey):
        decrypt(modified_encrypted_message, password)
