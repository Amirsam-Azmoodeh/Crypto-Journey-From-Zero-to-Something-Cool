"""
try12: Hashed Header + HMAC
----------------------------
Concept: Header is hashed, HMAC added
Security: LOW - Hashed header adds no real security
Author: Amirsam Azmoodeh
"""

import hashlib
import base64
import hmac
import os

def encrypt(data, key):
    salt = os.urandom(16)
    nonce = os.urandom(16)
    header = hashlib.sha256(b'\x43\x5A\x4C\x4F\x4E\x45\x44\x41' + b'\x00' + b'\x00\x00\x00').digest()
    soft_state = os.urandom(8)

    ciphertext = bytearray()

    kdf_salt = salt + soft_state
    state = hashlib.pbkdf2_hmac('sha256', key.encode(), kdf_salt, 600000, 32)

    block_counter = 0
    keystream = hmac.new(state, nonce + block_counter.to_bytes(8, 'big'), hashlib.sha256).digest()

    mac_key = hashlib.sha256(state + b"MAC").digest()

    data = data.encode('utf-8')
    counter = 0

    for byt in data:
        if counter == 32:
            block_counter += 1
            keystream = hmac.new(state, nonce + block_counter.to_bytes(8, 'big'), hashlib.sha256).digest()
            counter = 0

        ciphertext.append(keystream[counter] ^ byt)
        counter += 1

    tag = hmac.new(mac_key, soft_state + header + ciphertext, hashlib.sha256).digest()

    message = salt + nonce + soft_state + header + bytes(ciphertext) + tag

    return base64.b64encode(message).decode('ascii')


def decrypt(data, key):
    data = base64.b64decode(data)
    header = hashlib.sha256(b'\x43\x5A\x4C\x4F\x4E\x45\x44\x41' + b'\x00' + b'\x00\x00\x00').digest()

    plaintext = bytearray()
    salt = data[:16]
    nonce = data[16:32]
    soft_state = data[32:40]
    header2 = data[40:72]
    tag = data[-32:]
    data = data[72:-32]

    kdf_salt = salt + soft_state
    state = hashlib.pbkdf2_hmac('sha256', key.encode(), kdf_salt, 600000, 32)
    block_counter = 0
    keystream = hmac.new(state, nonce + block_counter.to_bytes(8, 'big'), hashlib.sha256).digest()

    mac_key = hashlib.sha256(state + b"MAC").digest()

    counter = 0

    expected_tag = hmac.new(mac_key, soft_state + header + data, hashlib.sha256).digest()

    if not hmac.compare_digest(expected_tag, tag) or header != header2:
        return

    for byt in data:
        if counter == 32:
            block_counter += 1
            keystream = hmac.new(state, nonce + block_counter.to_bytes(8, 'big'), hashlib.sha256).digest()
            counter = 0

        c = byt ^ keystream[counter]
        plaintext.append(c)
        counter += 1

    return plaintext.decode('utf-8')


# Example usage
print(encrypt('this is one test!', 'amirsam'))
print(decrypt('mQ1NQ+ACS2au0ndxXu/U97WXOEpErdPvKQPA37IFh7S2csXyHlU2HoqmvNMPwE2ZGO/XkLVA9yKMVnbrTrIk2p4S4X/BnEJpE9Mk8ljNl3i+Abzhoa0o/6BGPhWa', 'amirsam'))