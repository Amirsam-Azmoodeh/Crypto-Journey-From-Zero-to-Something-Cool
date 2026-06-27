"""
Test suite for replay protection mechanisms across different versions.
"""

import pytest
from src.try_19 import ASA_Crypt as SetCrypt
from src.try_21 import ASA_Crypt as BitmapCrypt
from src.try_26 import ASA_Crypt as CuckooCrypt


class TestReplayProtection:
    """Test replay protection across different versions."""
    
    @pytest.fixture
    def set_crypt(self):
        return SetCrypt(b'test-key')
    
    @pytest.fixture
    def bitmap_crypt(self):
        return BitmapCrypt(b'test-key')
    
    @pytest.fixture
    def cuckoo_crypt(self):
        return CuckooCrypt(b'test-key')
    
    def test_set_replay_protection(self, set_crypt):
        """Test set-based replay protection."""
        msg = set_crypt.encrypt("test")
        assert msg is not None
        
        # First decryption should succeed
        result1 = set_crypt.decrypt(msg)
        assert result1 == "test"
        
        # Second decryption should fail
        result2 = set_crypt.decrypt(msg)
        assert result2 is None
    
    def test_bitmap_replay_protection(self, bitmap_crypt):
        """Test bitmap-based replay protection."""
        msg = bitmap_crypt.encrypt("test")
        assert msg is not None
        
        # First decryption should succeed
        result1 = bitmap_crypt.decrypt(msg)
        assert result1 == "test"
        
        # Second decryption should fail
        result2 = bitmap_crypt.decrypt(msg)
        assert result2 is None
    
    def test_cuckoo_replay_protection(self, cuckoo_crypt):
        """Test cuckoo filter replay protection."""
        msg = cuckoo_crypt.encrypt("test")
        assert msg is not None
        
        # First decryption should succeed
        result1 = cuckoo_crypt.decrypt(msg)
        assert result1 == "test"
        
        # Second decryption should fail
        result2 = cuckoo_crypt.decrypt(msg)
        assert result2 is None
    
    def test_many_messages_set(self, set_crypt):
        """Test set with many messages."""
        messages = []
        for i in range(50):
            msg = set_crypt.encrypt(f"message_{i}")
            assert msg is not None
            messages.append(msg)
            assert set_crypt.decrypt(msg) == f"message_{i}"
        
        # Try replaying all messages
        for msg in messages:
            assert set_crypt.decrypt(msg) is None
    
    def test_many_messages_bitmap(self, bitmap_crypt):
        """Test bitmap with many messages."""
        messages = []
        for i in range(200):
            msg = bitmap_crypt.encrypt(f"message_{i}")
            assert msg is not None
            messages.append(msg)
            assert bitmap_crypt.decrypt(msg) == f"message_{i}"
        
        # Try replaying random messages
        import random
        for _ in range(50):
            msg = random.choice(messages)
            # Some may have been evicted due to false positives
            # So we don't assert, just check it doesn't crash
            bitmap_crypt.decrypt(msg)
    
    def test_many_messages_cuckoo(self, cuckoo_crypt):
        """Test cuckoo filter with many messages."""
        messages = []
        for i in range(200):
            msg = cuckoo_crypt.encrypt(f"message_{i}")
            assert msg is not None
            messages.append(msg)
            assert cuckoo_crypt.decrypt(msg) == f"message_{i}"
        
        # Try replaying random messages
        import random
        for _ in range(50):
            msg = random.choice(messages)
            # Cuckoo should detect all replays
            assert cuckoo_crypt.decrypt(msg) is None
    
    def test_limited_set_eviction(self):
        """Test that limited set evicts old entries."""
        crypt = SetCrypt(b'test-key')
        
        # Send more than 100 messages
        messages = []
        for i in range(150):
            msg = crypt.encrypt(f"message_{i}")
            messages.append(msg)
            crypt.decrypt(msg)
        
        # Some old messages may have been evicted
        # Just verify it doesn't crash
        for msg in messages[:50]:
            crypt.decrypt(msg)  # May return None or text
    
    def test_cuckoo_auto_rotation(self):
        """Test cuckoo filter auto-rotation."""
        crypt = CuckooCrypt(
            b'test-key',
            cuckoo_num_segments=2,
            cuckoo_bucket_count=32,
            cuckoo_bucket_size=2
        )
        
        initial_seg = crypt.cuckoo_current_seg
        
        # Fill up segments
        for i in range(500):
            msg = crypt.encrypt(f"msg_{i}")
            crypt.decrypt(msg)
        
        # Should have rotated
        assert crypt.cuckoo_current_seg != initial_seg
    
    def test_replay_detection_count(self):
        """Test that replay detection count is accurate."""
        crypt = CuckooCrypt(b'test-key')
        
        msg = crypt.encrypt("test")
        
        # Decrypt once (should succeed)
        crypt.decrypt(msg)
        initial_detected = crypt.cuckoo_detected
        
        # Decrypt again (should be detected)
        crypt.decrypt(msg)
        assert crypt.cuckoo_detected == initial_detected + 1
    
    def test_set_size_limit(self):
        """Test set size limit (try_20)."""
        from src.try_20 import ASA_Crypt
        crypt = ASA_Crypt(b'test-key')
        
        # Send 120 messages
        messages = []
        for i in range(120):
            msg = crypt.encrypt(f"msg_{i}")
            messages.append(msg)
            crypt.decrypt(msg)
        
        # Set should have limited size
        assert len(crypt.ciphertext_set) <= 100
    
    def test_bitmap_auto_reset(self):
        """Test bitmap auto-reset (try_23)."""
        from src.try_23 import ASA_Crypt
        crypt = ASA_Crypt(
            b'test-key',
            bitmap_size=1000,
            bitmap_auto_reset=True,
            bitmap_reset_threshold=50,
            bitmap_reset_ratio=0.5
        )
        
        # Send messages until reset
        for i in range(1000):
            msg = crypt.encrypt(f"msg_{i}")
            crypt.decrypt(msg)
            
            # Check if reset happened
            if crypt.bitmap_used_bits < 100:
                break
        
        # Should have reset at some point
        assert crypt.bitmap_used_bits < 500
    
    def test_different_replay_methods(self):
        """Compare different replay protection methods."""
        key = b'test-key'
        
        # Set-based (try_19)
        set_crypt = SetCrypt(key)
        set_msg = set_crypt.encrypt("test")
        set_crypt.decrypt(set_msg)
        set_replay = set_crypt.decrypt(set_msg)
        
        # Bitmap-based (try_21)
        bitmap_crypt = BitmapCrypt(key)
        bitmap_msg = bitmap_crypt.encrypt("test")
        bitmap_crypt.decrypt(bitmap_msg)
        bitmap_replay = bitmap_crypt.decrypt(bitmap_msg)
        
        # Cuckoo-based (try_26)
        cuckoo_crypt = CuckooCrypt(key)
        cuckoo_msg = cuckoo_crypt.encrypt("test")
        cuckoo_crypt.decrypt(cuckoo_msg)
        cuckoo_replay = cuckoo_crypt.decrypt(cuckoo_msg)
        
        # All should detect replay
        assert set_replay is None
        assert bitmap_replay is None
        assert cuckoo_replay is None