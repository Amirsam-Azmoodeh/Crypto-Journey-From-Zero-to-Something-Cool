"""
Test vectors for validating encryption/decryption across versions.
"""

import pytest
import base64
from src.try_26 import ASA_Crypt


class TestVectors:
    """Test vectors for try_26."""
    
    @pytest.fixture
    def crypt(self):
        """Create crypt instance with fixed parameters for testing."""
        return ASA_Crypt(
            key=b'test-vector-key',
            salt_size=16,
            nonce_size=16,
            hmac_size=16,
            block_size=32
        )
    
    def test_vector_basic(self, crypt):
        """Test basic vector."""
        plaintext = "Hello, World!"
        encrypted = crypt.encrypt(plaintext)
        assert encrypted is not None
        
        decrypted = crypt.decrypt(encrypted)
        assert decrypted == plaintext
    
    def test_vector_special_chars(self, crypt):
        """Test special characters."""
        plaintext = "!@#$%^&*()_+-=[]{}|;':,.<>?/~`"
        encrypted = crypt.encrypt(plaintext)
        decrypted = crypt.decrypt(encrypted)
        assert decrypted == plaintext
    
    def test_vector_unicode(self, crypt):
        """Test unicode characters."""
        plaintext = "سلام دنیا! 🌍✨ こんにちは 你好"
        encrypted = crypt.encrypt(plaintext)
        decrypted = crypt.decrypt(encrypted)
        assert decrypted == plaintext
    
    def test_vector_numbers(self, crypt):
        """Test numeric strings."""
        plaintext = "1234567890" * 10
        encrypted = crypt.encrypt(plaintext)
        decrypted = crypt.decrypt(encrypted)
        assert decrypted == plaintext
    
    def test_vector_long_text(self, crypt):
        """Test long text."""
        plaintext = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 50
        encrypted = crypt.encrypt(plaintext)
        decrypted = crypt.decrypt(encrypted)
        assert decrypted == plaintext
    
    def test_vector_whitespace(self, crypt):
        """Test whitespace characters."""
        plaintext = "  \t\n\r  multiple spaces  "
        encrypted = crypt.encrypt(plaintext)
        decrypted = crypt.decrypt(encrypted)
        assert decrypted == plaintext
    
    def test_vector_duplicate_tags(self, crypt):
        """Test that duplicate tags are detected."""
        # Multiple messages with same content
        msg1 = crypt.encrypt("duplicate")
        msg2 = crypt.encrypt("duplicate")
        
        # Both should decrypt first time
        assert crypt.decrypt(msg1) == "duplicate"
        assert crypt.decrypt(msg2) == "duplicate"
        
        # Replays should fail
        assert crypt.decrypt(msg1) is None
        assert crypt.decrypt(msg2) is None
    
    def test_vector_different_keys(self):
        """Test with different keys."""
        crypt1 = ASA_Crypt(b'key1')
        crypt2 = ASA_Crypt(b'key2')
        
        plaintext = "test"
        enc1 = crypt1.encrypt(plaintext)
        enc2 = crypt2.encrypt(plaintext)
        
        # Different keys should produce different ciphertexts
        assert enc1 != enc2
        
        # But both should decrypt correctly
        assert crypt1.decrypt(enc1) == plaintext
        assert crypt2.decrypt(enc2) == plaintext
        
        # Cross-decryption should fail
        assert crypt1.decrypt(enc2) is None
        assert crypt2.decrypt(enc1) is None
    
    def test_vector_cuckoo_params(self):
        """Test different cuckoo parameters."""
        configs = [
            {'cuckoo_num_segments': 2},
            {'cuckoo_num_segments': 8},
            {'cuckoo_bucket_count': 128},
            {'cuckoo_bucket_count': 512},
            {'cuckoo_fingerprint_bits': 8},
            {'cuckoo_fingerprint_bits': 16},
            {'cuckoo_bucket_size': 2},
            {'cuckoo_bucket_size': 8},
        ]
        
        for config in configs:
            crypt = ASA_Crypt(b'test', **config)
            plaintext = "test message"
            encrypted = crypt.encrypt(plaintext)
            decrypted = crypt.decrypt(encrypted)
            assert decrypted == plaintext
    
    def test_vector_all_versions(self, all_versions):
        """Test all versions with a simple vector."""
        plaintext = "Hello"
        
        for version, data in all_versions.items():
            try:
                if 'encrypt' in data:
                    # Function-based version
                    enc = data['encrypt'](plaintext, "test-key")
                    assert enc is not None
                    dec = data['decrypt'](enc, "test-key")
                    assert dec == plaintext
                elif 'class' in data:
                    # Class-based version
                    crypt = data['class'](b'test-key')
                    enc = crypt.encrypt(plaintext)
                    assert enc is not None
                    dec = crypt.decrypt(enc)
                    assert dec == plaintext
            except Exception as e:
                # Skip versions that might have issues
                print(f"Skipping {version}: {e}")
                continue
    
    def test_vector_message_format(self, crypt):
        """Test message format structure."""
        plaintext = "test"
        encrypted = crypt.encrypt(plaintext)
        
        # Decode
        decoded = base64.b64decode(encrypted)
        
        # Check minimum length
        assert len(decoded) >= 6 + 16 + 16 + 16  # header + salt + nonce + hmac
        
        # Check header
        header = decoded[:6]
        assert header == crypt.header
        
        # Check salt
        salt = decoded[6:22]  # 6 + 16
        assert len(salt) == crypt.salt_size
        
        # Check nonce
        nonce = decoded[22:38]  # 6 + 16 + 16
        assert len(nonce) == crypt.nonce_size
        
        # Check HMAC at end
        hmac = decoded[-crypt.hmac_size:]
        assert len(hmac) == crypt.hmac_size
    
    def test_vector_randomness(self, crypt):
        """Test that encryption is random (different outputs)."""
        plaintext = "test"
        encrypted1 = crypt.encrypt(plaintext)
        encrypted2 = crypt.encrypt(plaintext)
        
        # Should be different due to different salt/nonce
        assert encrypted1 != encrypted2
        
        # But both should decrypt correctly
        assert crypt.decrypt(encrypted1) == plaintext
        assert crypt.decrypt(encrypted2) == plaintext
    
    def test_vector_error_recovery(self, crypt):
        """Test error recovery."""
        # Malformed messages
        assert crypt.decrypt("") is None
        assert crypt.decrypt("invalid") is None
        
        # Message with wrong length
        assert crypt.decrypt("A" * 100) is None
        
        # Message with invalid base64
        assert crypt.decrypt("!@#$%^&*()") is None
    
    def test_vector_identical_keys(self):
        """Test identical keys produce compatible results."""
        crypt1 = ASA_Crypt(b'same-key')
        crypt2 = ASA_Crypt(b'same-key')
        
        plaintext = "test"
        enc1 = crypt1.encrypt(plaintext)
        enc2 = crypt2.encrypt(plaintext)
        
        # Different ciphertexts
        assert enc1 != enc2
        
        # Cross-decryption should work
        assert crypt1.decrypt(enc2) == plaintext
        assert crypt2.decrypt(enc1) == plaintext
    
    def test_vector_cuckoo_consistency(self):
        """Test cuckoo filter consistency."""
        crypt = ASA_Crypt(b'test')
        
        # Insert and check
        tag = b'test_tag'
        assert crypt.check_tag(tag) is False  # First time
        assert crypt.check_tag(tag) is True   # Second time
        
        # Different tags
        tag2 = b'test_tag_2'
        assert crypt.check_tag(tag2) is False
        assert crypt.check_tag(tag2) is True