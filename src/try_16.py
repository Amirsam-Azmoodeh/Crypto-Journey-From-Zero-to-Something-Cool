"""
try16: Fusion + Rotation
-------------------------
Concept: Added bit rotation and fusion function for key mixing
Security: MEDIUM - Experimental mixing, not cryptographically proven
Author: Amirsam Azmoodeh
"""

import hashlib
import base64
import hmac
import os

class ASA_Crypt:

    def __init__(self, key: str):
        self.header = b'\x43\x5A\x4C\x4F\x4E\x45\x44\x41' + b'\x00' + b'\x00\x00\x00'
        self.key = key.encode('utf-8')

    def rotate_bits(self, data: bytes, bits: int) -> bytes:
        number = int.from_bytes(data, 'big')
        total_bits = len(data) * 8
        bits = bits % total_bits

        left_part = number << bits
        right_part = number >> (total_bits - bits)

        result = left_part | right_part

        mask = (1 << total_bits) - 1
        result = result & mask

        return result.to_bytes(len(data), 'big')

    def fusion(self, salt, nonce, soft_state):
        rotated_salt = self.rotate_bits(salt, 5)
        rotated_nonce = self.rotate_bits(nonce, 13)

        stage1 = b''
        stage2 = b''
        stage3 = b''

        for i in range(len(rotated_salt)):
            byte1 = soft_state[i]
            byte2 = rotated_salt[i]
            xor = byte1 ^ byte2
            stage1 += bytes([xor])

        for i in range(len(salt)):
            byte1 = salt[i]
            byte2 = rotated_nonce[i]
            xor = byte1 ^ byte2
            stage2 += bytes([xor])

        number_nonce = int.from_bytes(nonce, 'big')
        number_soft = int.from_bytes(soft_state, 'big')

        total_bits = len(nonce) * 8
        mod_value = 1 << total_bits

        sum_value = (number_nonce + number_soft) % mod_value

        stage3 = sum_value.to_bytes(len(nonce), 'big')

        return stage1 + stage2 + stage3

    def create_state(self, salt: bytes, nonce: bytes, soft_state: bytes) -> bytes:
        mixed = self.fusion(salt, nonce, soft_state)
        state = hmac.new(self.key, mixed, hashlib.sha256).digest()
        return state

    def create_keystream(self, state: bytes, extra_string: bytes, nonce: bytes, block_counter: int) -> bytes:
        data = b'ASA-V1' + extra_string + nonce + block_counter.to_bytes(8, 'big') + bytes(extra_string[block_counter % len(extra_string)]) + bytes(nonce[block_counter % 16])
        return hashlib.blake2s(data, key=state).digest()

    def create_mac_key(self, state: bytes) -> bytes:
        return hashlib.sha256(state + b'ASA-MAC-1').digest()

    def create_hmac(self, mac_key: bytes, salt: bytes, nonce: bytes, soft_state: bytes, ciphertext: bytes) -> bytes:
        return hmac.new(mac_key, salt + nonce + soft_state + self.header + ciphertext, hashlib.sha256).digest()

    def encrypt(self, plaintext: str) -> str:
        try:
            salt = os.urandom(16)
            nonce = os.urandom(16)
            soft_state = os.urandom(16)
            plaintext = plaintext.encode('utf-8')
        except Exception:
            return

        ciphertext = bytearray()
        block_counter = 0
        counter = 0

        state = self.create_state(salt, nonce, soft_state)
        keystream = self.create_keystream(state, b'ASA-STREAM-V1', nonce, block_counter)
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
            return

        if len(ciphertext) < 92:
            return

        plaintext = bytearray()

        salt = ciphertext[:16]
        nonce = ciphertext[16:32]
        soft_state = ciphertext[32:48]
        header2 = ciphertext[48:60]
        tag = ciphertext[-32:]
        ciphertext = ciphertext[60:-32]

        block_counter = 0
        counter = 0

        state = self.create_state(salt, nonce, soft_state)
        keystream = self.create_keystream(state, b'ASA-STREAM-V1', nonce, block_counter)
        mac_key = self.create_mac_key(state)

        expected_tag = self.create_hmac(mac_key, salt, nonce, soft_state, ciphertext)

        if self.header != header2:
            return

        if not hmac.compare_digest(expected_tag, tag):
            return

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