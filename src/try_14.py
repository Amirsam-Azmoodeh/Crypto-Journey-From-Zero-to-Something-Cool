"""
try14: Class-based Architecture
-------------------------------
Concept: OOP design with proper documentation
Security: LOW - Better structure but same vulnerabilities
Author: Amirsam Azmoodeh
"""

import hashlib
import base64
import hmac
import os

class ASA_Crypt:

    def __init__(self, key: str):
        self.header = b'\x43\x5A\x4C\x4F\x4E\x45\x44\x41' + b'\x00' + b'\x00\x00\x00'
        self.key = key

    def create_state(self, salt: bytes, soft_state: bytes) -> bytes:
        kdf_salt = salt + soft_state
        state = hashlib.pbkdf2_hmac('sha256', self.key.encode(), kdf_salt, 500000, 32)
        return state

    def create_keystream(self, state: bytes, extra_string: bytes, nonce: bytes, block_counter: int) -> bytes:
        keystream = hmac.new((state + b'ENCRYPT'), extra_string + nonce + block_counter.to_bytes(8, 'big'), hashlib.sha256).digest()
        return keystream

    def create_mac_key(self, state: bytes) -> bytes:
        return hashlib.sha256(state + b"MAC").digest()

    def create_hmac(self, mac_key: bytes, salt: bytes, nonce: bytes, soft_state: bytes, ciphertext: bytes) -> bytes:
        return hmac.new(mac_key, salt + nonce + soft_state + self.header + ciphertext, hashlib.sha256).digest()

    def encrypt(self, plaintext: str) -> str:
        try:
            salt = os.urandom(16)
            nonce = os.urandom(16)
            soft_state = os.urandom(8)
            plaintext = plaintext.encode('utf-8')
        except Exception as e:
            raise ValueError(f'Encryption initialization failed: {e}')

        ciphertext = bytearray()
        block_counter = 0
        counter = 0

        state = self.create_state(salt, soft_state)
        keystream = self.create_keystream(state, b'EXTRA STRING', nonce, block_counter)
        mac_key = self.create_mac_key(state)

        for byt in plaintext:
            if counter == 32:
                block_counter += 1
                keystream = self.create_keystream(state, keystream, nonce, block_counter)
                counter = 0

            ciphertext.append(keystream[counter] ^ byt)
            counter += 1

        tag = self.create_hmac(mac_key, salt, nonce, soft_state, ciphertext)

        message = salt + nonce + soft_state + self.header + bytes(ciphertext) + tag

        return base64.b64encode(message).decode('ascii')

    def decrypt(self, ciphertext: str) -> str:
        try:
            ciphertext = base64.b64decode(ciphertext)
        except Exception:
            return 'invalid base64 input'

        if len(ciphertext) < 84:
            return 'ciphertext too short'

        plaintext = bytearray()

        salt = ciphertext[:16]
        nonce = ciphertext[16:32]
        soft_state = ciphertext[32:40]
        header2 = ciphertext[40:52]
        tag = ciphertext[-32:]
        ciphertext = ciphertext[52:-32]

        block_counter = 0
        counter = 0

        state = self.create_state(salt, soft_state)
        keystream = self.create_keystream(state, b'EXTRA STRING', nonce, block_counter)
        mac_key = self.create_mac_key(state)

        expected_tag = self.create_hmac(mac_key, salt, nonce, soft_state, ciphertext)

        if self.header != header2:
            return 'header mismatch'

        if not hmac.compare_digest(expected_tag, tag):
            return 'tag mismatch'

        for byt in ciphertext:
            if counter == 32:
                block_counter += 1
                keystream = self.create_keystream(state, keystream, nonce, block_counter)
                counter = 0

            plaintext.append(byt ^ keystream[counter])
            counter += 1

        return plaintext.decode('utf-8', errors='replace')


# Example usage
crypt = ASA_Crypt('amirsam')
print(crypt.encrypt('this is one test!'))