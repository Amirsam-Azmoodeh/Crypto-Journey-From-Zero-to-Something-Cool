"""
try21: Bitmap-based Replay Protection
--------------------------------------
Concept: Replaced set with bitmap for memory efficiency
Security: MEDIUM-HIGH - Bitmap has false positive possibility
Author: Amirsam Azmoodeh | Ehsan Bakhtiari(Bitmap implementation)
"""

import hashlib
import base64
import hmac
import os
from bitarray import bitarray


class ASA_Crypt:

    def __init__(self, key: bytes, bitmap_size: int = 65536):
        self.header = b'\x12\x12\x0C' + b'\x01' + b'\x00' + b'\x00'
        self.key = key
        self.bitmap_size = bitmap_size
        self.bitmap = bitarray(bitmap_size)
        self.bitmap.setall(False)

    def create_key(self, num: int) -> bytes:
        return os.urandom(num)

    def create_state(self, salt: bytes) -> bytes:
        state = hmac.new(self.key, salt + b'ASA-V1', hashlib.sha256).digest()
        return state

    def create_keystream(self, state: bytes, nonce: bytes, block_counter: int) -> bytes:
        data = nonce + b'ASA-STREAM-V1' + block_counter.to_bytes(8, 'big')
        return hashlib.blake2s(data+b'ENC', key=state).digest()

    def create_mac_key(self, state: bytes) -> bytes:
        mac_key = hmac.new(state, b'MAC', hashlib.sha256).digest()
        return hmac.new(mac_key, b'ASA-MAC-1', hashlib.sha256).digest()

    def create_hmac(self, mac_key: bytes, salt: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
        return hmac.new(mac_key, salt + nonce + self.header + ciphertext, hashlib.sha256).digest()[:16]

    def encrypt(self, plaintext: str) -> str:
        try:
            salt = os.urandom(13)
            nonce = os.urandom(13)
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

        message = self.header + salt + nonce + bytes(ciphertext) + tag

        return base64.b64encode(message).decode('ascii')

    def tag_index(self, tag: bytes) -> int:
        return int.from_bytes(hashlib.blake2s(tag).digest()[:12], 'big') % self.bitmap_size

    def check_tag(self, tag: bytes) -> bool:
        index = self.tag_index(tag)

        if self.bitmap[index]:
            return True

        self.bitmap[index] = True
        return False

    def decrypt(self, full_message: str) -> str:
        try:
            full_message = base64.b64decode(full_message)
        except Exception:
            return

        if len(full_message) < 50 or len(full_message) > 4096 + 50:
            return

        plaintext = bytearray()

        header2 = full_message[:6]
        salt = full_message[6:19]
        nonce = full_message[19:32]
        ciphertext = full_message[32:-16]
        tag = full_message[-16:]

        block_counter = 0
        counter = 0

        state = self.create_state(salt)
        keystream = self.create_keystream(state, nonce, block_counter)
        mac_key = self.create_mac_key(state)

        expected_tag = self.create_hmac(mac_key, salt, nonce, ciphertext)

        if not hmac.compare_digest(self.header, header2):
            return

        if not hmac.compare_digest(expected_tag, tag):
            return

        if self.check_tag(tag):
            return

        for byt in ciphertext:
            if counter == 32:
                block_counter += 1
                keystream = self.create_keystream(state, nonce, block_counter)
                counter = 0

            plaintext.append(byt ^ keystream[counter])
            counter += 1

        return plaintext.decode('utf-8', errors='replace')


# Example usage
crypt = ASA_Crypt(b'amirsam')
print(crypt.encrypt('this is one test!'))