"""
try22: Bitmap-based Replay Protection
------------------------------------
Concept: Replaced set with bitmap for memory efficiency
Security: MEDIUM-HIGH - Bitmap has false positive possibility
Author: Amirsam Azmoodeh | Ehsan Bakhtiari (Bitmap implementation)
"""

import hashlib
import base64
import hmac
import os
from bitarray import bitarray


class ASA_Crypt:
    """ASA Cryptography class for encryption/decryption operations."""
    
    def __init__(self, key: bytes, salt_size: int = 16, nonce_size: int = 16, hmac_size: int = 16, block_size: int = 32, min_size: int = 0, max_size: int = 4096, bitmap_size: int = 65536):
        """Initialize the ASA_Crypt instance.
        
        Args:
            key: Encryption key
            salt_size: Size of salt in bytes
            nonce_size: Size of nonce in bytes
            hmac_size: Size of HMAC in bytes
            block_size: Size of each keystream block
            min_size: Minimum allowed message size
            max_size: Maximum allowed message size
            bitmap_size: Size of the bitmap for tag tracking
        """
        self.header = b'\x12\x12\x0C' + b'\x01' + b'\x00' + b'\x00'
        self.key = key
        self.salt_size = salt_size
        self.nonce_size = nonce_size
        self.hmac_size = hmac_size
        self.block_size = block_size
        self.min_size = min_size
        self.max_size = max_size
        self.bitmap_size = bitmap_size
        self.bitmap = bitarray(bitmap_size)
        self.bitmap.setall(False)
    
    def create_key(self, num: int) -> bytes:
        """Create a random key of specified length.
        
        Args:
            num: Length of the key to generate
            
        Returns:
            Random bytes of length num
        """
        return os.urandom(num)
    
    def create_state(self, salt: bytes) -> bytes:
        """Create the initial state using HMAC.
        
        Args:
            salt: Salt value for state generation
            
        Returns:
            State bytes
        """
        state = hmac.new(self.key, salt + b'ASA-V1', hashlib.sha256).digest()
        return state
    
    def create_keystream(self, state: bytes, nonce: bytes, block_counter: int) -> bytes:
        """Generate keystream for encryption/decryption.
        
        Args:
            state: Current state
            nonce: Nonce value
            block_counter: Current block counter
            
        Returns:
            Keystream bytes
        """
        data = nonce + b'ASA-STREAM-V1' + block_counter.to_bytes(8, 'big')
        return hashlib.blake2s(data, key=state).digest()
    
    def create_mac_key(self, state: bytes) -> bytes:
        """Create MAC key from state.
        
        Args:
            state: Current state
            
        Returns:
            MAC key bytes
        """
        mac_key = hmac.new(state, b'MAC', hashlib.sha256).digest()
        return hmac.new(mac_key, b'ASA-MAC-1', hashlib.sha256).digest()
    
    def create_hmac(self, mac_key: bytes, salt: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
        """Create HMAC for authentication.
        
        Args:
            mac_key: MAC key
            salt: Salt value
            nonce: Nonce value
            ciphertext: Encrypted data
            
        Returns:
            HMAC digest (first 16 bytes)
        """
        return hmac.new(mac_key, salt + nonce + self.header + ciphertext, hashlib.sha256).digest()[:self.hmac_size]
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext string.
        
        Args:
            plaintext: Text to encrypt
            
        Returns:
            Base64 encoded encrypted message
        """
        try:
            salt = os.urandom(self.salt_size)
            nonce = os.urandom(self.nonce_size)
            plaintext = plaintext.encode('utf-8')
        except Exception:
            return
        
        ciphertext = bytearray()
        block_counter = 0
        counter = 0
        
        state = self.create_state(salt)
        keystream = self.create_keystream(state, nonce, block_counter)
        mac_key = self.create_mac_key(state)
        
        for byte in plaintext:
            if counter == self.block_size:
                block_counter += 1
                keystream = self.create_keystream(state, nonce, block_counter)
                counter = 0
            
            ciphertext.append(keystream[counter] ^ byte)
            counter += 1
        
        tag = self.create_hmac(mac_key, salt, nonce, ciphertext)
        message = self.header + salt + nonce + bytes(ciphertext) + tag
        
        return base64.b64encode(message).decode('ascii')
    
    def tag_index(self, tag: bytes) -> int:
        """Calculate bitmap index for a tag.
        
        Args:
            tag: Tag bytes
            
        Returns:
            Index in bitmap
        """
        return int.from_bytes(hashlib.blake2s(tag).digest()[:12], 'big') % self.bitmap_size
    
    def check_tag(self, tag: bytes) -> bool:
        """Check if tag has been seen before.
        
        Args:
            tag: Tag to check
            
        Returns:
            True if tag already exists (replay detected), False otherwise
        """
        index = self.tag_index(tag)
        
        if self.bitmap[index]:
            return True
        
        self.bitmap[index] = True
        return False
    
    def decrypt(self, full_message: str) -> str:
        """Decrypt encrypted message.
        
        Args:
            full_message: Base64 encoded encrypted message
            
        Returns:
            Decrypted plaintext string
        """
        try:
            full_message = base64.b64decode(full_message)
        except Exception:
            return
        
        plaintext = bytearray()
        
        header2 = full_message[:6]
        salt = full_message[6:6 + self.salt_size]
        nonce = full_message[6 + self.salt_size: 6 + self.salt_size + self.nonce_size]
        ciphertext = full_message[6 + self.salt_size + self.nonce_size:-self.hmac_size]
        tag = full_message[-self.hmac_size:]
        
        block_counter = 0
        counter = 0
        
        state = self.create_state(salt)
        keystream = self.create_keystream(state, nonce, block_counter)
        mac_key = self.create_mac_key(state)
        expected_tag = self.create_hmac(mac_key, salt, nonce, ciphertext)
        
        valid = True
        valid &= len(full_message) >= self.min_size
        valid &= len(full_message) <= self.max_size
        valid &= hmac.compare_digest(self.header, header2)
        valid &= hmac.compare_digest(expected_tag, tag)
        valid &= not self.check_tag(tag)
        
        if not valid:
            return
        
        for byte in ciphertext:
            if counter == self.block_size:
                block_counter += 1
                keystream = self.create_keystream(state, nonce, block_counter)
                counter = 0
            
            plaintext.append(byte ^ keystream[counter])
            counter += 1
        
        return plaintext.decode('utf-8', errors='replace')
