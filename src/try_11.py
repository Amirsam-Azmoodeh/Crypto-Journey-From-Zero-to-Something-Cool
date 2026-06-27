"""
try11: PBKDF2 + Soft State (1 Byte)
------------------------------------
Concept: Added 1-byte soft_state to KDF salt
Security: LOW - 1 byte soft_state is too small
Author: Amirsam Azmoodeh
"""

import hashlib
import base64
import hmac
import os

def encrypt(data, key):
    salt = os.urandom(16)
    nonce = os.urandom(16)
    MAGIC = b'\x43\x5A\x4C\x4F\x4E\x45\x44\x41' + b'\x00' + b'\x00\x00\x00'
    soft_state = os.urandom(1)

    ciphertext = bytearray()
    encrypt_header = bytearray(12)

    kdf_salt = salt + soft_state
    state = hashlib.pbkdf2_hmac('sha256', key.encode(), kdf_salt, 600000, 32)

    block_counter = 0
    keystream = hmac.new(state, nonce + block_counter.to_bytes(8, 'big'), hashlib.sha256).digest()

    mac_key = hashlib.sha256(state + b"MAC").digest()

    data = data.encode('utf-8')
    counter = 0

    for i in range(12):
        encrypt_header[i] = (MAGIC[i] ^ keystream[counter])
        counter += 1

    for byt in data:
        if counter == 32:
            block_counter += 1
            keystream = hmac.new(state, nonce + block_counter.to_bytes(8, 'big'), hashlib.sha256).digest()
            counter = 0

        ciphertext.append(keystream[counter] ^ byt)
        counter += 1

    tag = hmac.new(mac_key, soft_state + encrypt_header + ciphertext, hashlib.sha256).digest()

    message = salt + nonce + soft_state + encrypt_header + bytes(ciphertext) + tag

    return base64.b64encode(message).decode('ascii')


def decrypt(data, key):
    data = base64.b64decode(data)
    MAGIC = b'\x43\x5A\x4C\x4F\x4E\x45\x44\x41' + b'\x00' + b'\x00\x00\x00'

    plaintext = bytearray()
    header = bytearray(12)
    salt = data[:16]
    nonce = data[16:32]
    soft_state = data[32:33]
    encrypt_header = data[33:45]
    tag = data[-32:]
    data = data[45:-32]

    kdf_salt = salt + soft_state
    state = hashlib.pbkdf2_hmac('sha256', key.encode(), kdf_salt, 600000, 32)
    block_counter = 0
    keystream = hmac.new(state, nonce + block_counter.to_bytes(8, 'big'), hashlib.sha256).digest()

    mac_key = hashlib.sha256(state + b"MAC").digest()

    counter = 0

    for i in range(12):
        header[i] = (encrypt_header[i] ^ keystream[counter])
        counter += 1

    expected_tag = hmac.new(mac_key, soft_state + encrypt_header + data, hashlib.sha256).digest()

    if header != MAGIC or expected_tag != tag:
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
print(decrypt('a91PsOR8kcztAAPT2Y8aH6n7n+4q9Xtdh9l41YyZzK65J9ufHAivS0kZJCndgmwM0SBeU0wlxQ5Ftt1jT7K42m/ykoD2NUT/ck57bq8shGrYejbWEJZXdQsFaokpsg==', 'amirsam'))