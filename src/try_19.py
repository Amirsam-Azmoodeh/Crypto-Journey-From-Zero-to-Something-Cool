"""
try19: Set-based Replay Protection (Fixed)
-------------------------------------------
Concept: Fixed set bug, replay protection works
Security: MEDIUM - Set works but memory inefficient
Author: Amirsam Azmoodeh
"""

import hashlib
import base64
import hmac
import os

class ASA_Crypt:

    def __init__(self, key: bytes):
        self.header = b'\x43\x5A\x4C\x4F\x4E\x45\x44\x41' + b'\x00' + b'\x00\x00\x00'
        self.key = key
        self.ciphertext_set = set()

    def create_key(self, num: int) -> bytes:
        return os.urandom(num)

    def create_state(self, salt: bytes) -> bytes:
        state = hmac.new(self.key, salt + b'ASA-V1', hashlib.sha256).digest()
        return state

    def create_keystream(self, state: bytes, nonce: bytes, block_counter: int) -> bytes:
        data = nonce + b'ASA-STREAM-V1' + block_counter.to_bytes(8, 'big')
        return hashlib.blake2s(data, key=state).digest()

    def create_mac_key(self, state: bytes) -> bytes:
        mac_key = hmac.new(state, b'MAC', hashlib.sha256).digest()
        return hmac.new(mac_key, b'ASA-MAC-1', hashlib.sha256).digest()

    def create_hmac(self, mac_key: bytes, salt: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
        return hmac.new(mac_key, salt + nonce + self.header + ciphertext, hashlib.sha256).digest()

    def encrypt(self, plaintext: str) -> str:
        try:
            salt = os.urandom(16)
            nonce = os.urandom(12)
            plaintext = plaintext.encode('utf-8')
        except Exception:
            return

        ciphertext = bytearray()
        block_counter = 0
        counter = 0

        state = self.create_state(salt)
        keystream = self.create_keystream(state, nonce, block_counter)
        mac_key = self.create_mac_key(state)

        for byt in plaintext:
            if counter == 32:
                block_counter += 1
                keystream = self.create_keystream(state, nonce, block_counter)
                counter = 0

            ciphertext.append(keystream[counter] ^ byt)
            counter += 1

        tag = self.create_hmac(mac_key, salt, nonce, ciphertext)

        message = salt + nonce + self.header + bytes(ciphertext) + tag

        return base64.b64encode(message).decode('ascii')

    def decrypt(self, full_message: str) -> str:
        try:
            full_message = base64.b64decode(full_message)
        except Exception:
            return

        if len(full_message) < 72 or len(full_message) > 4096 + 72:
            return

        plaintext = bytearray()

        salt = full_message[:16]
        nonce = full_message[16:28]
        header2 = full_message[28:40]
        ciphertext = full_message[40:-32]
        tag = full_message[-32:]

        block_counter = 0
        counter = 0

        state = self.create_state(salt)
        keystream = self.create_keystream(state, nonce, block_counter)
        mac_key = self.create_mac_key(state)

        expected_tag = self.create_hmac(mac_key, salt, nonce, ciphertext)

        if self.header != header2:
            return

        if not hmac.compare_digest(expected_tag, tag):
            return

        if tag in self.ciphertext_set:
            return

        for byt in ciphertext:
            if counter == 32:
                block_counter += 1
                keystream = self.create_keystream(state, nonce, block_counter)
                counter = 0

            plaintext.append(byt ^ keystream[counter])
            counter += 1

        if len(self.ciphertext_set) >= 100:
            self.ciphertext_set.pop()

        self.ciphertext_set.add(tag)

        return plaintext.decode('utf-8', errors='replace')


# Example usage
crypt = ASA_Crypt(b'amirsam')
print(crypt.encrypt('this is one test!'))