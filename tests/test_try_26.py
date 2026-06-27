"""
Test suite for try_26 - Cuckoo Filter + Blake2b
"""

import pytest
from src.try_26 import ASA_Crypt


class TestTry26:
    """Test cases for try_26 implementation."""
    
    @pytest.fixture
    def crypt(self):
        """Create a crypt instance for testing."""
        return ASA_Crypt(b'test-key-123')
    
    def test_encrypt_decrypt(self, crypt):
        """Test basic encryption and decryption."""
        plaintext = "Hello, World!"
        encrypted = crypt.encrypt(plaintext)
        assert encrypted is not None
        assert isinstance(encrypted, str)
        
        decrypted = crypt.decrypt(encrypted)
        assert decrypted == plaintext
    
    def test_replay_protection(self, crypt):
        """Test that replay attacks are detected."""
        msg = crypt.encrypt("test message")
        assert msg is not None
        
        # First decryption should work
        result1 = crypt.decrypt(msg)
        assert result1 == "test message"
        
        # Second decryption should fail (replay)
        result2 = crypt.decrypt(msg)
        assert result2 is None
    
    def test_cuckoo_filter_stats(self, crypt):
        """Test cuckoo filter statistics."""
        # Send messages
        for i in range(100):
            msg = crypt.encrypt(f"message_{i}")
            crypt.decrypt(msg)
        
        # Check stats
        assert crypt.cuckoo_total_checks >= 100
        assert crypt.cuckoo_detected >= 0
    
    def test_empty_message(self, crypt):
        """Test encryption/decryption of empty string."""
        encrypted = crypt.encrypt("")
        assert encrypted is not None
        
        decrypted = crypt.decrypt(encrypted)
        assert decrypted == ""
    
    def test_long_message(self, crypt):
        """Test encryption of long messages."""
        plaintext = "A" * 10000
        encrypted = crypt.encrypt(plaintext)
        assert encrypted is not None
        
        decrypted = crypt.decrypt(encrypted)
        assert decrypted == plaintext
    
    def test_invalid_decrypt(self, crypt):
        """Test decryption of invalid data."""
        assert crypt.decrypt("invalid_base64!") is None
        assert crypt.decrypt("") is None
        assert crypt.decrypt("short") is None
        assert crypt.decrypt("a" * 1000) is None
    
    def test_different_keys(self):
        """Test that different keys produce different results."""
        crypt1 = ASA_Crypt(b'key1')
        crypt2 = ASA_Crypt(b'key2')
        
        plaintext = "test"
        enc1 = crypt1.encrypt(plaintext)
        enc2 = crypt2.encrypt(plaintext)
        
        assert enc1 != enc2
        
        dec1 = crypt1.decrypt(enc1)
        dec2 = crypt2.decrypt(enc2)
        assert dec1 == dec2 == plaintext
    
    def test_cuckoo_configuration(self):
        """Test different cuckoo filter configurations."""
        configs = [
            {'cuckoo_num_segments': 2},
            {'cuckoo_num_segments': 8},
            {'cuckoo_bucket_count': 128},
            {'cuckoo_bucket_count': 512},
            {'cuckoo_fingerprint_bits': 8},
            {'cuckoo_fingerprint_bits': 16},
        ]
        
        for config in configs:
            crypt = ASA_Crypt(b'test', **config)
            msg = crypt.encrypt("test")
            assert msg is not None
            assert crypt.decrypt(msg) == "test"
    
    def test_header_validation(self, crypt):
        """Test header validation."""
        msg = crypt.encrypt("test")
        # Tamper with header
        import base64
        decoded = base64.b64decode(msg)
        # Change first byte
        tampered = base64.b64encode(b'\x00' + decoded[1:])
        result = crypt.decrypt(tampered.decode())
        assert result is None
    
    def test_hmac_validation(self, crypt):
        """Test HMAC validation."""
        msg = crypt.encrypt("test")
        # Tamper with ciphertext
        import base64
        decoded = base64.b64decode(msg)
        # Change a byte in ciphertext
        decoded = bytearray(decoded)
        decoded[40] = decoded[40] ^ 0xFF
        tampered = base64.b64encode(bytes(decoded))
        result = crypt.decrypt(tampered.decode())
        assert result is None
    
    def test_unicode(self, crypt):
        """Test unicode characters."""
        plaintext = "سلام دنیا! 🌍✨ こんにちは 你好"
        encrypted = crypt.encrypt(plaintext)
        assert encrypted is not None
        
        decrypted = crypt.decrypt(encrypted)
        assert decrypted == plaintext
    
    def test_whitespace(self, crypt):
        """Test whitespace characters."""
        plaintext = "  \t\n\r  multiple spaces  "
        encrypted = crypt.encrypt(plaintext)
        decrypted = crypt.decrypt(encrypted)
        assert decrypted == plaintext
    
    def test_special_chars(self, crypt):
        """Test special characters."""
        plaintext = "!@#$%^&*()_+-=[]{}|;':,.<>?/~`"
        encrypted = crypt.encrypt(plaintext)
        decrypted = crypt.decrypt(encrypted)
        assert decrypted == plaintext
    
    def test_numeric(self, crypt):
        """Test numeric strings."""
        plaintext = "1234567890" * 10
        encrypted = crypt.encrypt(plaintext)
        decrypted = crypt.decrypt(encrypted)
        assert decrypted == plaintext
    
    def test_salt_size(self):
        """Test different salt sizes."""
        for size in [12, 16, 24, 32]:
            crypt = ASA_Crypt(b'test', salt_size=size)
            assert crypt.salt_size == size
            msg = crypt.encrypt("test")
            assert crypt.decrypt(msg) == "test"
    
    def test_nonce_size(self):
        """Test different nonce sizes."""
        for size in [12, 16, 24, 32]:
            crypt = ASA_Crypt(b'test', nonce_size=size)
            assert crypt.nonce_size == size
            msg = crypt.encrypt("test")
            assert crypt.decrypt(msg) == "test"
    
    def test_hmac_size(self):
        """Test different HMAC sizes."""
        for size in [8, 12, 16, 24, 32]:
            crypt = ASA_Crypt(b'test', hmac_size=size)
            assert crypt.hmac_size == size
            msg = crypt.encrypt("test")
            assert crypt.decrypt(msg) == "test"
    
    def test_block_size(self):
        """Test different block sizes."""
        for size in [16, 32, 64, 128]:
            crypt = ASA_Crypt(b'test', block_size=size)
            assert crypt.block_size == size
            msg = crypt.encrypt("test")
            assert crypt.decrypt(msg) == "test"
    
    def test_cuckoo_enabled(self):
        """Test with cuckoo filter disabled."""
        crypt = ASA_Crypt(b'test', cuckoo_enabled=False)
        msg = crypt.encrypt("test")
        assert crypt.decrypt(msg) == "test"
        
        # Replay should work (no protection)
        assert crypt.decrypt(msg) == "test"
    
    def test_cuckoo_disabled_stats(self):
        """Test stats when cuckoo filter is disabled."""
        crypt = ASA_Crypt(b'test', cuckoo_enabled=False)
        assert crypt.cuckoo_total_checks == 0
        assert crypt.cuckoo_detected == 0
    
    def test_message_size_limits(self):
        """Test min and max message size limits."""
        # Min size
        crypt = ASA_Crypt(b'test', min_size=100, max_size=200)
        msg = crypt.encrypt("A" * 50)
        assert crypt.decrypt(msg) is None
        
        # Max size
        crypt = ASA_Crypt(b'test', min_size=0, max_size=100)
        msg = crypt.encrypt("A" * 200)
        assert crypt.decrypt(msg) is None
        
        # Valid size
        crypt = ASA_Crypt(b'test', min_size=0, max_size=100)
        msg = crypt.encrypt("A" * 50)
        assert crypt.decrypt(msg) == "A" * 50
    
    def test_multiple_instances(self):
        """Test multiple crypt instances."""
        crypt1 = ASA_Crypt(b'key1')
        crypt2 = ASA_Crypt(b'key1')  # Same key
        
        msg1 = crypt1.encrypt("test")
        msg2 = crypt2.encrypt("test")
        
        # Different ciphertexts (different salt/nonce)
        assert msg1 != msg2
        
        # But both decrypt correctly
        assert crypt1.decrypt(msg1) == "test"
        assert crypt2.decrypt(msg2) == "test"
        
        # Cross-decryption should fail
        assert crypt1.decrypt(msg2) is None
        assert crypt2.decrypt(msg1) is None
    
    def test_encrypt_error_handling(self, crypt):
        """Test error handling in encrypt."""
        # Invalid key type
        with pytest.raises(Exception):
            ASA_Crypt("not bytes")  # Should raise TypeError
    
    def test_decrypt_error_handling(self, crypt):
        """Test error handling in decrypt."""
        # Invalid base64
        assert crypt.decrypt("not valid base64!!!") is None
        
        # Empty string
        assert crypt.decrypt("") is None
        
        # Too short
        assert crypt.decrypt("short") is None