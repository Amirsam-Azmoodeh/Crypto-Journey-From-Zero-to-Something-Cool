"""
try25: Cuckoo Filter Implementation
------------------------------------
Concept: Replaced bitmap with cuckoo filter for replay protection
Security: HIGH - Very low false positive rate, no false negatives
Author: Amirsam Azmoodeh | Ehsan Bakhtiari (Bitmap implementation)
"""

import hashlib
import base64
import hmac
import os
import random


class ASA_Crypt:
    """ASA Cryptography class for encryption/decryption operations."""
    
    def __init__(self, key: bytes, salt_size: int = 16, nonce_size: int = 16, hmac_size: int = 16, block_size: int = 32, min_size: int = 0, max_size: int = 4096, cuckoo_num_segments: int = 4, cuckoo_bucket_count: int = 256, cuckoo_bucket_size: int = 4, cuckoo_fingerprint_bits: int = 12, cuckoo_buckets_per_tag: int = 2, cuckoo_kicking_attempts: int = 100):
        """Initialize the ASA_Crypt instance.
        
        Args:
            key: Encryption key
            salt_size: Size of salt in bytes
            nonce_size: Size of nonce in bytes
            hmac_size: Size of HMAC in bytes
            block_size: Size of each keystream block
            min_size: Minimum allowed message size
            max_size: Maximum allowed message size
            cuckoo_num_segments: Number of segments in cuckoo filter
            cuckoo_bucket_count: Number of buckets per segment
            cuckoo_bucket_size: Number of slots per bucket
            cuckoo_fingerprint_bits: Bits used for fingerprint
            cuckoo_buckets_per_tag: Number of buckets per tag
            cuckoo_kicking_attempts: Max kicks during insertion
        """
        self.header = b'\x12\x12\x0C' + b'\x01' + b'\x00' + b'\x00'
        self.key = key
        self.salt_size = salt_size
        self.nonce_size = nonce_size
        self.hmac_size = hmac_size
        self.block_size = block_size
        self.min_size = min_size
        self.max_size = max_size
        self.cuckoo_num_segments = cuckoo_num_segments
        self.cuckoo_bucket_count = cuckoo_bucket_count
        self.cuckoo_bucket_size = cuckoo_bucket_size
        self.cuckoo_fingerprint_bits = cuckoo_fingerprint_bits
        self.cuckoo_buckets_per_tag = cuckoo_buckets_per_tag
        self.cuckoo_kicking_attempts = cuckoo_kicking_attempts
        self.cuckoo_segments = []
        for _ in range(self.cuckoo_num_segments):
            segment = []
            for _ in range(self.cuckoo_bucket_count):
                row = [None] * self.cuckoo_bucket_size
                segment.append(row)
            self.cuckoo_segments.append(segment)
        self.cuckoo_current_seg = 0
        self.cuckoo_total_checks = 0
        self.cuckoo_detected = 0

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
        data = nonce + block_counter.to_bytes(8, 'big')
        return hashlib.blake2s(data, key=state).digest()

    def process_nonce(self, nonce: bytes, salt: bytes) -> bytes:
        """Process nonce using HMAC.
        
        Args:
            nonce: Original nonce
            salt: Salt value
            
        Returns:
            Processed nonce bytes
        """
        return hmac.new(self.key, nonce + salt + b'NONCE', hashlib.sha256).digest()[:self.nonce_size]
    
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
        
        early_nonce = nonce
        nonce = self.process_nonce(nonce, salt)

        for byte in plaintext:
            if counter == self.block_size:
                block_counter += 1
                keystream = self.create_keystream(state, nonce, block_counter)
                counter = 0
            
            ciphertext.append(keystream[counter] ^ byte)
            counter += 1
        
        tag = self.create_hmac(mac_key, salt, early_nonce, ciphertext)
        message = self.header + salt + early_nonce + bytes(ciphertext) + tag
        
        return base64.b64encode(message).decode('ascii')

    def check_tag(self, tag: bytes) -> bool:
        """Check if tag has been seen before using cuckoo filter.
        
        Args:
            tag: Tag to check
            
        Returns:
            True if tag already exists (replay detected), False otherwise
        """
        self.cuckoo_total_checks += 1
        
        if self.cuckoo_add_to_segment(self.cuckoo_current_seg, tag):
            self.cuckoo_detected += 1
            return True
        
        for i in range(1, self.cuckoo_num_segments):
            seg_idx = (self.cuckoo_current_seg - i) % self.cuckoo_num_segments
            if self.cuckoo_exists_in_segment(seg_idx, tag):
                self.cuckoo_detected += 1
                return True
        
        if self.cuckoo_is_segment_full(self.cuckoo_current_seg):
            self.cuckoo_rotate()
        
        return False

    def cuckoo_fingerprint_and_buckets(self, tag: bytes = None, fingerprint: int = None) -> tuple:
        """Generate fingerprint and bucket indices for a tag."""
        if tag is not None:
            h = hashlib.blake2s(tag).digest()
            fingerprint = int.from_bytes(h[0:2], 'big')
            max_fp = (1 << self.cuckoo_fingerprint_bits) - 1
            fingerprint = fingerprint & max_fp
        elif fingerprint is None:
            raise ValueError("Either tag or fingerprint must be provided")
        
        k = self.cuckoo_buckets_per_tag
        
        if k == 2:
            if tag is not None:
                bucket1 = int.from_bytes(h[2:4], 'big') % self.cuckoo_bucket_count
            else:
                bucket1 = fingerprint % self.cuckoo_bucket_count
            
            GOLDEN_RATIO = 0x9e3779b9
            bucket2 = (bucket1 ^ (fingerprint * GOLDEN_RATIO)) % self.cuckoo_bucket_count
            
            if bucket2 == bucket1:
                bucket2 = (bucket2 + 1) % self.cuckoo_bucket_count
            
            return (fingerprint, [bucket1, bucket2])
        
        buckets = []
        for i in range(k):
            if tag is not None:
                offset = 2 + (i * 2)
                if offset + 2 > len(h):
                    if len(h) > 2:
                        offset = offset % (len(h) - 2)
                    else:
                        offset = 0
                bucket = int.from_bytes(h[offset:offset+2], 'big')
                bucket = bucket % self.cuckoo_bucket_count
                if i > 0:
                    bucket = (bucket ^ (fingerprint * (i + 1))) % self.cuckoo_bucket_count
            else:
                bucket = (fingerprint ^ (i * 0x9e3779b9)) % self.cuckoo_bucket_count
            
            if bucket not in buckets:
                buckets.append(bucket)
        
        while len(buckets) < k:
            new_bucket = (buckets[-1] + 1) % self.cuckoo_bucket_count
            if new_bucket not in buckets:
                buckets.append(new_bucket)
        
        return (fingerprint, buckets)

    def cuckoo_exists_in_segment(self, seg_idx: int, tag: bytes) -> bool:
        """Check if fingerprint exists in a segment."""
        fingerprint, buckets = self.cuckoo_fingerprint_and_buckets(tag)
        segment = self.cuckoo_segments[seg_idx]
        
        for bucket in buckets:
            for slot in range(self.cuckoo_bucket_size):
                if segment[bucket][slot] == fingerprint:
                    return True
        return False

    def cuckoo_add_to_segment(self, seg_idx: int, tag: bytes) -> bool:
        """Add fingerprint to a segment. Returns True if duplicate found."""
        fingerprint, buckets = self.cuckoo_fingerprint_and_buckets(tag)
        segment = self.cuckoo_segments[seg_idx]
        
        for bucket in buckets:
            for slot in range(self.cuckoo_bucket_size):
                if segment[bucket][slot] == fingerprint:
                    return True
        
        for bucket in buckets:
            for slot in range(self.cuckoo_bucket_size):
                if segment[bucket][slot] is None:
                    segment[bucket][slot] = fingerprint
                    return False
        
        current_fp = fingerprint
        current_bucket = buckets[0]
        
        for _ in range(self.cuckoo_kicking_attempts):
            slot = random.randint(0, self.cuckoo_bucket_size - 1)
            
            old_fp = segment[current_bucket][slot]
            segment[current_bucket][slot] = current_fp
            current_fp = old_fp
            
            _, new_buckets = self.cuckoo_fingerprint_and_buckets(fingerprint=current_fp)

            for new_bucket in new_buckets:
                for slot2 in range(self.cuckoo_bucket_size):
                    if segment[new_bucket][slot2] is None:
                        segment[new_bucket][slot2] = current_fp
                        return False

            current_bucket = new_buckets[0]

        return False

    def cuckoo_rotate(self):
        """Rotate to next segment and clear it."""
        self.cuckoo_current_seg = (self.cuckoo_current_seg + 1) % self.cuckoo_num_segments
        segment = self.cuckoo_segments[self.cuckoo_current_seg]
        for bucket in range(self.cuckoo_bucket_count):
            for slot in range(self.cuckoo_bucket_size):
                segment[bucket][slot] = None

    def cuckoo_is_segment_full(self, seg_idx: int) -> bool:
        """Check if a segment is nearly full."""
        segment = self.cuckoo_segments[seg_idx]
        total_cells = self.cuckoo_bucket_count * self.cuckoo_bucket_size
        used = 0
        for bucket in range(self.cuckoo_bucket_count):
            for slot in range(self.cuckoo_bucket_size):
                if segment[bucket][slot] is not None:
                    used += 1
        return (used / total_cells) > 0.95

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
        
        nonce = self.process_nonce(nonce, salt)
        
        for byte in ciphertext:
            if counter == self.block_size:
                block_counter += 1
                keystream = self.create_keystream(state, nonce, block_counter)
                counter = 0
            
            plaintext.append(byte ^ keystream[counter])
            counter += 1
        
        return plaintext.decode('utf-8', errors='replace')
