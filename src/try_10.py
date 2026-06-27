"""
try10: Header + HMAC Authentication
------------------------------------
Concept: Added header for protocol identification, HMAC for integrity
Security: LOW - Now with authentication
Author: Amirsam Azmoodeh
"""

import hashlib
import base64
import hmac
import os

def encrypt(data , key) :
    salt = os.urandom(16)
    nonce = os.urandom(16)
    MAGIC = b'\x43\x5A\x4C\x4F\x4E\x45\x44\x41' + b'\x00' + b'\x00\x00\x00'

    ciphertext = bytearray()
    encrypt_header = bytearray(12)
    state = hashlib.pbkdf2_hmac('sha256', key.encode(), salt, 600000, 32)
    block_counter = 0
    keystream = hashlib.sha256(state + nonce + block_counter.to_bytes(8,'big')).digest()

    mac_key = hashlib.sha256(state + b"MAC").digest()

    data = data.encode('utf-8')
    
    counter = 0

    # Encrypt header with keystream
    for i in range(12) :
        encrypt_header[i] = (MAGIC[i] ^ keystream[counter])
        counter += 1

    # Encrypt data
    for byt in data :
        if counter == 32:
            block_counter += 1
            keystream = hashlib.sha256(keystream + nonce + block_counter.to_bytes(8,'big')).digest()
            counter = 0

        ciphertext.append(keystream[counter] ^ byt)
        counter += 1

    # Generate authentication tag
    tag = hmac.new(mac_key, encrypt_header + ciphertext, hashlib.sha256).digest()

    return base64.b64encode(salt + nonce + encrypt_header + bytes(ciphertext) + tag).decode('ascii')

 
def decrypt(data , key) :
    data = base64.b64decode(data)
    MAGIC = b'\x43\x5A\x4C\x4F\x4E\x45\x44\x41' + b'\x00' + b'\x00\x00\x00'

    plaintext = bytearray()
    header = bytearray(12)
    salt = data[:16]
    nonce = data[16:32]
    encrypt_header = data[32:44]
    tag = data[-32:]
    data = data[44:-32]

    state = hashlib.pbkdf2_hmac('sha256', key.encode(), salt, 600000, 32)
    block_counter = 0
    keystream = hashlib.sha256(state + nonce + block_counter.to_bytes(8,'big')).digest()

    mac_key = hashlib.sha256(state + b"MAC").digest()

    counter = 0

    # Decrypt header
    for i in range(12) :
        header[i] = (encrypt_header[i] ^ keystream[counter])
        counter += 1

    # Verify tag
    expected_tag = hmac.new(mac_key, encrypt_header + data, hashlib.sha256).digest()

    if header != MAGIC or expected_tag != tag :
        return
    
    # Decrypt data
    for byt in data :
        if counter == 32:
            block_counter += 1
            keystream = hashlib.sha256(keystream + nonce + block_counter.to_bytes(8,'big')).digest()
            counter = 0

        c = byt ^ keystream[counter]
        plaintext.append(c)
        counter += 1

    return plaintext.decode('utf-8')
    

# Example usage
print(encrypt('this is one test!' , 'amirsam') )
print(decrypt('mQ1NQ+ACS2au0ndxXu/U97WXOEpErdPvKQPA37IFh7S2csXyHlU2HoqmvNMPwE2ZGO/XkLVA9yKMVnbrTrIk2p4S4X/BnEJpE9Mk8ljNl3i+Abzhoa0o/6BGPhWa' , 'amirsam'))