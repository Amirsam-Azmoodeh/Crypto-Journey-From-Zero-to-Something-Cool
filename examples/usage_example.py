"""
Usage Example for Crypto-Journey
================================
This file demonstrates how to use the most advanced version (try_26)
with various configurations and features.
"""

import sys
from pathlib import Path

# Add parent directory to path to import src
sys.path.append(str(Path(__file__).parent.parent))

from src.try_26 import ASA_Crypt


def basic_usage():
    """Demonstrate basic encryption and decryption."""
    print("\n" + "="*60)
    print("🔐 BASIC USAGE EXAMPLE")
    print("="*60)
    
    # Create crypt instance with default settings
    crypt = ASA_Crypt(key=b'my-secret-key-123')
    
    # Encrypt a message
    plaintext = "Hello, World! This is a secure message."
    print(f"📝 Plaintext: {plaintext}")
    
    encrypted = crypt.encrypt(plaintext)
    print(f"🔒 Encrypted: {encrypted[:50]}...")
    
    # Decrypt the message
    decrypted = crypt.decrypt(encrypted)
    print(f"🔓 Decrypted: {decrypted}")
    
    # Verify
    assert decrypted == plaintext
    print("✅ Encryption/Decryption successful!")


def replay_protection_demo():
    """Demonstrate replay protection feature."""
    print("\n" + "="*60)
    print("🛡️ REPLAY PROTECTION DEMONSTRATION")
    print("="*60)
    
    crypt = ASA_Crypt(key=b'replay-test-key')
    
    # Encrypt a message
    message = "This is a one-time message"
    encrypted = crypt.encrypt(message)
    print(f"📝 Original: {message}")
    print(f"🔒 Encrypted: {encrypted[:50]}...")
    
    # First decryption - should work
    result1 = crypt.decrypt(encrypted)
    print(f"✅ First decryption: {result1}")
    
    # Second decryption - should fail (replay detected)
    result2 = crypt.decrypt(encrypted)
    print(f"❌ Second decryption: {result2} (Replay detected!)")
    
    # Show statistics
    print(f"\n📊 Cuckoo Filter Stats:")
    print(f"   Total checks: {crypt.cuckoo_total_checks}")
    print(f"   Replays detected: {crypt.cuckoo_detected}")


def custom_configuration():
    """Demonstrate custom configuration options."""
    print("\n" + "="*60)
    print("⚙️ CUSTOM CONFIGURATION EXAMPLE")
    print("="*60)
    
    # High security configuration
    crypt_high = ASA_Crypt(
        key=b'high-security-key',
        salt_size=32,              # Larger salt
        nonce_size=24,             # Larger nonce
        hmac_size=32,              # Full HMAC
        block_size=64,             # Larger block
        cuckoo_num_segments=8,     # More segments
        cuckoo_bucket_count=1024,  # More buckets
        cuckoo_fingerprint_bits=16 # More fingerprint bits
    )
    
    print("🔒 High Security Configuration:")
    print(f"   Salt Size: {crypt_high.salt_size} bytes")
    print(f"   Nonce Size: {crypt_high.nonce_size} bytes")
    print(f"   HMAC Size: {crypt_high.hmac_size} bytes")
    print(f"   Block Size: {crypt_high.block_size} bytes")
    print(f"   Cuckoo Segments: {crypt_high.cuckoo_num_segments}")
    print(f"   Cuckoo Buckets: {crypt_high.cuckoo_bucket_count}")
    print(f"   Fingerprint Bits: {crypt_high.cuckoo_fingerprint_bits}")
    
    # Test with high security config
    plaintext = "High security message"
    encrypted = crypt_high.encrypt(plaintext)
    decrypted = crypt_high.decrypt(encrypted)
    print(f"✅ Test successful: {decrypted}")
    
    # Memory optimized configuration
    crypt_low = ASA_Crypt(
        key=b'memory-optimized-key',
        salt_size=12,
        nonce_size=12,
        hmac_size=12,
        block_size=32,
        cuckoo_num_segments=2,
        cuckoo_bucket_count=128,
        cuckoo_fingerprint_bits=8
    )
    
    print("\n💾 Memory Optimized Configuration:")
    print(f"   Salt Size: {crypt_low.salt_size} bytes")
    print(f"   Nonce Size: {crypt_low.nonce_size} bytes")
    print(f"   HMAC Size: {crypt_low.hmac_size} bytes")
    print(f"   Cuckoo Segments: {crypt_low.cuckoo_num_segments}")
    
    # Test with memory optimized config
    encrypted = crypt_low.encrypt("Memory optimized")
    decrypted = crypt_low.decrypt(encrypted)
    print(f"✅ Test successful: {decrypted}")


def batch_processing():
    """Demonstrate processing multiple messages."""
    print("\n" + "="*60)
    print("📦 BATCH PROCESSING EXAMPLE")
    print("="*60)
    
    crypt = ASA_Crypt(key=b'batch-key')
    messages = [
        "Message 1: Hello",
        "Message 2: World",
        "Message 3: Crypto",
        "Message 4: Journey",
        "Message 5: Learning"
    ]
    
    encrypted_messages = []
    print("📝 Encrypting messages...")
    for msg in messages:
        encrypted = crypt.encrypt(msg)
        encrypted_messages.append(encrypted)
        print(f"   {msg[:20]} → {encrypted[:30]}...")
    
    print("\n🔓 Decrypting messages...")
    for i, enc in enumerate(encrypted_messages):
        decrypted = crypt.decrypt(enc)
        print(f"   {i+1}. {decrypted}")
    
    print(f"\n📊 Total messages processed: {len(messages)}")
    print(f"   Cuckoo checks: {crypt.cuckoo_total_checks}")
    print(f"   Replays detected: {crypt.cuckoo_detected}")


def error_handling():
    """Demonstrate error handling."""
    print("\n" + "="*60)
    print("⚠️ ERROR HANDLING EXAMPLE")
    print("="*60)
    
    crypt = ASA_Crypt(key=b'test-key')
    
    # Test with invalid input
    print("Testing invalid inputs...")
    
    # Invalid base64
    result = crypt.decrypt("invalid_base64!")
    print(f"   Invalid base64: {result} (should be None)")
    
    # Empty string
    result = crypt.decrypt("")
    print(f"   Empty string: {result} (should be None)")
    
    # Wrong key (different crypt instance)
    crypt2 = ASA_Crypt(key=b'different-key')
    msg = crypt.encrypt("Secret")
    result = crypt2.decrypt(msg)
    print(f"   Wrong key decryption: {result} (should be None)")
    
    # Encrypt empty string
    encrypted = crypt.encrypt("")
    decrypted = crypt.decrypt(encrypted)
    print(f"   Empty string encryption: '{decrypted}'")


def cuckoo_filter_stats():
    """Demonstrate cuckoo filter statistics."""
    print("\n" + "="*60)
    print("📊 CUCKOO FILTER STATISTICS")
    print("="*60)
    
    crypt = ASA_Crypt(
        key=b'stats-key',
        cuckoo_num_segments=4,
        cuckoo_bucket_count=256
    )
    
    # Simulate many messages
    num_messages = 200
    print(f"📤 Sending {num_messages} messages...")
    
    messages = []
    for i in range(num_messages):
        msg = crypt.encrypt(f"Message_{i}")
        messages.append(msg)
        crypt.decrypt(msg)
    
    # Try replaying some messages
    print("🔄 Testing replay detection...")
    replay_attempts = 50
    for i in range(replay_attempts):
        crypt.decrypt(messages[i % len(messages)])
    
    # Display statistics
    print("\n📈 Statistics:")
    print(f"   Total messages: {num_messages}")
    print(f"   Replay attempts: {replay_attempts}")
    print(f"   Total checks: {crypt.cuckoo_total_checks}")
    print(f"   Replays detected: {crypt.cuckoo_detected}")
    
    if crypt.cuckoo_total_checks > 0:
        rate = (crypt.cuckoo_detected / crypt.cuckoo_total_checks) * 100
        print(f"   Detection rate: {rate:.2f}%")


def main():
    """Run all examples."""
    print("🚀 CRYPTO-JOURNEY EXAMPLES")
    print("A 26-Step Journey from Basic XOR to Cuckoo Filters")
    print("="*60)
    
    try:
        basic_usage()
        replay_protection_demo()
        custom_configuration()
        batch_processing()
        error_handling()
        cuckoo_filter_stats()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60)
        print("\n💡 Tip: Try modifying the configurations to see how they affect")
        print("   performance and security. Check the docs/ directory for more")
        print("   information about each version's evolution.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()