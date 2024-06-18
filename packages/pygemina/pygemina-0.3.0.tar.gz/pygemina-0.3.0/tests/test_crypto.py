import string

import pytest

from gemina import *


def test_with_password():
    password = b'topsecret'
    data = string.ascii_letters.encode()
    enc_data = encrypt_with_password(password, data)
    assert data == decrypt_with_password(password, enc_data)
    with pytest.raises(DecryptError):
        decrypt_with_password(b'', enc_data)
    assert verify_with_password(password, enc_data)
    assert not verify_with_password(b'', enc_data)
    assert not verify_with_password(password, enc_data[:-1] + b'X')
    assert not verify_with_password(password, enc_data[:-30] + b'X' + enc_data[-29:])


def test_with_key():
    key = create_secret_key()
    assert len(key) == 32
    data = string.ascii_letters.encode()
    enc_data = encrypt_with_key(key, data)
    assert data == decrypt_with_key(key, enc_data)
    with pytest.raises(ValueError, match='incorrect secret key size'):
        decrypt_with_key(b'0' * 31, enc_data)
    with pytest.raises(DecryptError):
        decrypt_with_key(b'0' * 32, enc_data)
    assert verify_with_key(key, enc_data)
    assert not verify_with_key(b'0' * 32, enc_data)
    assert not verify_with_key(key, enc_data[:-1] + b'0')
    assert not verify_with_key(key, enc_data[:-30] + b'0' + enc_data[-29:])


@pytest.mark.parametrize('version', list(Version))
def test_with_password_version(version):
    password = b'topsecret'
    data = string.ascii_letters.encode()
    enc_data = encrypt_with_password(password, data, version=version)
    assert data == decrypt_with_password(password, enc_data)
    assert verify_with_password(password, enc_data)


@pytest.mark.parametrize('version, enc_key_len, mac_key_len',
                         list(zip(Version, [16, 16, 24, 32, 32], [16, 32, 32, 32, 32])))
def test_with_key_version(version, enc_key_len, mac_key_len):
    key = create_secret_key(version=version)
    assert len(key) == enc_key_len + mac_key_len
    data = string.ascii_letters.encode()
    enc_data = encrypt_with_key(key, data, version=version)
    assert data == decrypt_with_key(key, enc_data)
    assert verify_with_key(key, enc_data)
