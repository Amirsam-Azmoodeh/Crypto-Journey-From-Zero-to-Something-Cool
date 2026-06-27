
```markdown
# 🦆 Cuckoo Filter Deep Dive

## Introduction

A Cuckoo Filter is a probabilistic data structure used for membership testing. It's used in this project for **replay protection** - detecting if a message has been seen before.

## Why Cuckoo Filter?

### Comparison with Alternatives

| Method | Memory | False Positives | False Negatives | Operations |
|--------|--------|-----------------|-----------------|------------|
| **Set** | High (100%) | 0% | 0% | O(1) |
| **Bitmap** | Low (8KB) | ~0.001% | 0% | O(1) |
| **Bloom Filter** | Low | ~1% | 0% | O(k) |
| **Cuckoo Filter** | Medium (16KB) | ~0.01% | 0% | O(1) |

### Why Cuckoo is Better

1. **Supports Deletion**: Unlike Bloom filters
2. **Low False Positive**: ~0.01% vs 1%
3. **Balanced Memory**: Better than set, more accurate than bitmap
4. **No False Negatives**: Always finds items it has stored

## How Cuckoo Filter Works

### 1. Core Concepts

```python
class CuckooFilter:
    def __init__(self, num_segments=4, bucket_count=256, 
                 bucket_size=4, fingerprint_bits=12):
        self.num_segments = num_segments
        self.bucket_count = bucket_count
        self.bucket_size = bucket_size
        self.fingerprint_bits = fingerprint_bits
        
        # Create segments with buckets
        self.segments = []
        for _ in range(num_segments):
            segment = [[None] * bucket_size for _ in range(bucket_count)]
            self.segments.append(segment)
```

### 2. Fingerprint Generation

```python
def generate_fingerprint(self, tag):
    """Generate a fingerprint from a tag."""
    # Hash the tag
    h = hashlib.blake2s(tag).digest()
    # Take first 12 bits as fingerprint
    fingerprint = int.from_bytes(h[0:2], 'big')
    max_fp = (1 << self.fingerprint_bits) - 1
    return fingerprint & max_fp
```

**Fingerprint Size**: 12 bits (4,096 possible values)

### 3. Bucket Selection

```python
def get_alternate_buckets(self, fingerprint):
    """Get two bucket indices for a fingerprint."""
    # Primary bucket (based on fingerprint)
    bucket1 = fingerprint % self.bucket_count
    
    # Secondary bucket (using XOR with golden ratio)
    GOLDEN_RATIO = 0x9e3779b9
    bucket2 = (bucket1 ^ (fingerprint * GOLDEN_RATIO)) % self.bucket_count
    
    return [bucket1, bucket2]
```

### 4. Insertion Process

```python
def insert(self, tag):
    """Insert a tag into the cuckoo filter."""
    fingerprint = self.generate_fingerprint(tag)
    buckets = self.get_alternate_buckets(fingerprint)
    
    # Try to insert in any bucket
    for bucket in buckets:
        for slot in range(self.bucket_size):
            if self.segment[bucket][slot] is None:
                self.segment[bucket][slot] = fingerprint
                return True
    
    # If all buckets full, kick existing
    current_fp = fingerprint
    current_bucket = buckets[0]
    
    for attempt in range(self.kicking_attempts):
        # Pick random slot
        slot = random.randint(0, self.bucket_size - 1)
        
        # Kick existing fingerprint
        old_fp = self.segment[current_bucket][slot]
        self.segment[current_bucket][slot] = current_fp
        current_fp = old_fp
        
        # Get alternate bucket for kicked item
        _, new_buckets = self.get_alternate_buckets(current_fp)
        
        # Try to insert kicked item
        for new_bucket in new_buckets:
            for slot2 in range(self.bucket_size):
                if self.segment[new_bucket][slot2] is None:
                    self.segment[new_bucket][slot2] = current_fp
                    return True
        
        current_bucket = new_buckets[0]
    
    # Could not insert after max kicks
    return False
```

### 5. Lookup Process

```python
def exists(self, tag):
    """Check if a tag exists in the cuckoo filter."""
    fingerprint = self.generate_fingerprint(tag)
    buckets = self.get_alternate_buckets(fingerprint)
    
    for bucket in buckets:
        for slot in range(self.bucket_size):
            if self.segment[bucket][slot] == fingerprint:
                return True
    
    return False
```

### 6. Deletion Process

```python
def delete(self, tag):
    """Delete a tag from the cuckoo filter."""
    fingerprint = self.generate_fingerprint(tag)
    buckets = self.get_alternate_buckets(fingerprint)
    
    for bucket in buckets:
        for slot in range(self.bucket_size):
            if self.segment[bucket][slot] == fingerprint:
                self.segment[bucket][slot] = None
                return True
    
    return False
```

## Segment Rotation

### Why Rotate?

Memory is limited. Without rotation, the filter would eventually fill up and reject all new insertions.

### How Rotation Works

```python
def rotate_segments(self):
    """Rotate to next segment and clear it."""
    self.current_segment = (self.current_segment + 1) % self.num_segments
    # Clear the segment
    segment = self.segments[self.current_segment]
    for bucket in range(self.bucket_count):
        for slot in range(self.bucket_size):
            segment[bucket][slot] = None
```

### When to Rotate?

```python
def is_segment_full(self, segment_index):
    """Check if a segment is nearly full."""
    segment = self.segments[segment_index]
    total_cells = self.bucket_count * self.bucket_size
    used = sum(1 for row in segment for cell in row if cell is not None)
    return (used / total_cells) > 0.95  # 95% threshold
```

## Mathematics Behind Cuckoo Filters

### False Positive Rate

The false positive rate for a cuckoo filter is:

```
P(false positive) = (1 / 2^fingerprint_bits) * (1 / bucket_size)
```

For our configuration:
- fingerprint_bits = 12
- bucket_size = 4

```
P = (1 / 2^12) * (1/4) = 1 / 16384 ≈ 0.006%
```

### Memory Usage

```
Memory = num_segments × bucket_count × bucket_size × fingerprint_bits bits
```

For our configuration:
```
Memory = 4 × 256 × 4 × 12 = 49,152 bits = 6 KB (plus overhead)
```

### Load Factor

```
Load Factor = (num_items) / (num_segments × bucket_count × bucket_size)
```

At 95% load, the filter will rotate.

## Configuration Parameters

### num_segments (Default: 4)

- **More segments**: More memory, better accuracy
- **Fewer segments**: Less memory, faster

### bucket_count (Default: 256)

- **More buckets**: Lower false positive rate
- **Fewer buckets**: Less memory

### bucket_size (Default: 4)

- **Larger buckets**: Better for high load
- **Smaller buckets**: Less memory

### fingerprint_bits (Default: 12)

- **More bits**: Lower false positive rate
- **Fewer bits**: Less memory

## Performance Characteristics

### Time Complexity

- **Insert**: O(1) amortized
- **Lookup**: O(1)
- **Delete**: O(1)

### Space Complexity

- O(n) where n is number of items stored

## Advantages vs Bloom Filter

| Feature | Bloom Filter | Cuckoo Filter |
|---------|--------------|---------------|
| Deletion | ❌ | ✅ |
| False Positive Rate | Higher | Lower |
| Memory | Less | More |
| Speed | Fast | Fast |

## Implementation in try_26

```python
class ASA_Crypt:
    def __init__(self, key: bytes, ...):
        self.cuckoo_enabled = True
        self.cuckoo_num_segments = 4
        self.cuckoo_bucket_count = 256
        self.cuckoo_bucket_size = 4
        self.cuckoo_fingerprint_bits = 12
        self.cuckoo_kicking_attempts = 100
        
        # Initialize segments
        self.cuckoo_segments = [
            [[None] * self.cuckoo_bucket_size 
             for _ in range(self.cuckoo_bucket_count)]
            for _ in range(self.cuckoo_num_segments)
        ]
        
        self.cuckoo_current_seg = 0
        self.cuckoo_total_checks = 0
        self.cuckoo_detected = 0
    
    def check_tag(self, tag: bytes) -> bool:
        """Check if tag has been seen before."""
        self.cuckoo_total_checks += 1
        
        # Check current segment
        if self.cuckoo_add_to_segment(self.cuckoo_current_seg, tag):
            self.cuckoo_detected += 1
            return True
        
        # Check other segments
        for i in range(1, self.cuckoo_num_segments):
            seg_idx = (self.cuckoo_current_seg - i) % self.cuckoo_num_segments
            if self.cuckoo_exists_in_segment(seg_idx, tag):
                self.cuckoo_detected += 1
                return True
        
        # Rotate if current segment is full
        if self.cuckoo_is_segment_full(self.cuckoo_current_seg):
            self.cuckoo_rotate()
        
        return False
```

## Testing Cuckoo Filter

```python
def test_cuckoo_filter():
    crypt = ASA_Crypt(b'test')
    
    # Test insertion
    tag = b'test_tag'
    assert crypt.check_tag(tag) is False  # Not seen before
    assert crypt.check_tag(tag) is True   # Seen before
    
    # Test many insertions
    for i in range(1000):
        tag = f"tag_{i}".encode()
        assert crypt.check_tag(tag) is False
    
    # Test false positive rate
    false_positives = 0
    for i in range(10000):
        tag = f"nonexistent_{i}".encode()
        if crypt.check_tag(tag):
            false_positives += 1
    
    rate = false_positives / 10000
    print(f"False positive rate: {rate * 100:.2f}%")
    assert rate < 0.01  # Should be < 1%
```

## Visual Example

### Insertion Process

```
Step 1: Insert "A"
┌─────────────┐
│ Bucket 1    │
│ [A, _, _, _]│
└─────────────┘

Step 2: Insert "B" (same bucket)
┌─────────────┐
│ Bucket 1    │
│ [A, B, _, _]│
└─────────────┘

Step 3: Insert "C" (bucket full)
┌─────────────┐
│ Bucket 1    │  ← Full!
│ [A, B, C, _]│
└─────────────┘
          ↓ Kick "A"
┌─────────────┐
│ Bucket 1    │
│ [C, B, _, _]│
└─────────────┘
┌─────────────┐
│ Bucket 2    │  ← Insert "A" here
│ [A, _, _, _]│
└─────────────┘
```

## Conclusion

The Cuckoo Filter provides an excellent balance between:
- ✅ Memory efficiency
- ✅ Low false positive rate
- ✅ No false negatives
- ✅ Support for deletion
- ✅ Fast operations

This makes it ideal for replay protection in the Crypto-Journey project.

## References

- [Cuckoo Filter Paper](https://www.cs.cmu.edu/~dga/papers/cuckoo-conext2014.pdf)
- [Bloom Filter vs Cuckoo Filter](https://www.cs.cmu.edu/~dga/papers/cuckoo-conext2014.pdf)
- [Cuckoo Hashing](https://en.wikipedia.org/wiki/Cuckoo_hashing)
```

---

## 📄 پیام ۴: docs/api_reference.md

```markdown
# 📚 API Reference

## Overview

This document provides detailed API documentation for the most advanced version of Crypto-Journey: `try_26`.

---

## ASA_Crypt Class

### Constructor

```python
ASA_Crypt(
    key: bytes,
    salt_size: int = 16,
    nonce_size: int = 16,
    hmac_size: int = 16,
    block_size: int = 64,
    min_size: int = 0,
    max_size: int = 4096,
    cuckoo_enabled: bool = True,
    cuckoo_num_segments: int = 4,
    cuckoo_bucket_count: int = 256,
    cuckoo_bucket_size: int = 4,
    cuckoo_fingerprint_bits: int = 12,
    cuckoo_buckets_per_tag: int = 2,
    cuckoo_kicking_attempts: int = 100
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `key` | bytes | Required | Encryption key (should be cryptographically random) |
| `salt_size` | int | 16 | Size of salt in bytes |
| `nonce_size` | int | 16 | Size of nonce in bytes |
| `hmac_size` | int | 16 | Size of HMAC in bytes |
| `block_size` | int | 64 | Size of each keystream block |
| `min_size` | int | 0 | Minimum allowed message size |
| `max_size` | int | 4096 | Maximum allowed message size |
| `cuckoo_enabled` | bool | True | Enable cuckoo filter replay protection |
| `cuckoo_num_segments` | int | 4 | Number of segments in cuckoo filter |
| `cuckoo_bucket_count` | int | 256 | Number of buckets per segment |
| `cuckoo_bucket_size` | int | 4 | Number of slots per bucket |
| `cuckoo_fingerprint_bits` | int | 12 | Bits used for fingerprint |
| `cuckoo_buckets_per_tag` | int | 2 | Number of buckets per tag |
| `cuckoo_kicking_attempts` | int | 100 | Max kicks during insertion |

#### Example

```python
from src.try_26 import ASA_Crypt

# Create crypt instance
crypt = ASA_Crypt(
    key=b'my-secret-key-123',
    salt_size=32,
    nonce_size=24,
    cuckoo_num_segments=8
)
```

---

## Methods

### encrypt()

```python
def encrypt(self, plaintext: str) -> str
```

Encrypt plaintext string.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `plaintext` | str | Text to encrypt |

#### Returns

| Type | Description |
|------|-------------|
| str | Base64 encoded encrypted message |

#### Raises

| Exception | Description |
|-----------|-------------|
| None | Returns `None` on error |

#### Example

```python
plaintext = "Hello, World!"
encrypted = crypt.encrypt(plaintext)
print(encrypted)  # Base64 encoded ciphertext
```

---

### decrypt()

```python
def decrypt(self, full_message: str) -> str
```

Decrypt encrypted message.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `full_message` | str | Base64 encoded encrypted message |

#### Returns

| Type | Description |
|------|-------------|
| str | Decrypted plaintext string |

#### Raises

| Exception | Description |
|-----------|-------------|
| None | Returns `None` on error |

#### Example

```python
decrypted = crypt.decrypt(encrypted)
print(decrypted)  # "Hello, World!"
```

---

### check_tag()

```python
def check_tag(self, tag: bytes) -> bool
```

Check if tag has been seen before using cuckoo filter.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `tag` | bytes | Tag to check |

#### Returns

| Type | Description |
|------|-------------|
| bool | `True` if tag already exists (replay detected), `False` otherwise |

#### Example

```python
tag = b'test_tag'
is_replay = crypt.check_tag(tag)
if is_replay:
    print("Replay detected!")
```

---

### create_state()

```python
def create_state(self, salt: bytes) -> bytes
```

Create the initial state using Blake2s.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `salt` | bytes | Salt value for state generation |

#### Returns

| Type | Description |
|------|-------------|
| bytes | State bytes |

---

### create_keystream()

```python
def create_keystream(self, state: bytes, nonce: bytes, block_counter: int) -> bytes
```

Generate keystream using Blake2b.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `state` | bytes | Current state |
| `nonce` | bytes | Nonce value |
| `block_counter` | int | Current block counter |

#### Returns

| Type | Description |
|------|-------------|
| bytes | Keystream bytes |

---

### create_mac_key()

```python
def create_mac_key(self, state: bytes) -> bytes
```

Create MAC key from state.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `state` | bytes | Current state |

#### Returns

| Type | Description |
|------|-------------|
| bytes | MAC key bytes |

---

### create_hmac()

```python
def create_hmac(self, mac_key: bytes, salt: bytes, nonce: bytes, ciphertext: bytes) -> bytes
```

Create HMAC for authentication.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `mac_key` | bytes | MAC key |
| `salt` | bytes | Salt value |
| `nonce` | bytes | Nonce value |
| `ciphertext` | bytes | Encrypted data |

#### Returns

| Type | Description |
|------|-------------|
| bytes | HMAC digest (first `hmac_size` bytes) |

---

## Cuckoo Filter Methods

### cuckoo_fingerprint_and_buckets()

```python
def cuckoo_fingerprint_and_buckets(self, tag: bytes = None, fingerprint: int = None) -> tuple
```

Generate fingerprint and bucket indices for a tag.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `tag` | bytes | Tag to process |
| `fingerprint` | int | Existing fingerprint (optional) |

#### Returns

| Type | Description |
|------|-------------|
| tuple | `(fingerprint, [buckets])` |

---

### cuckoo_exists_in_segment()

```python
def cuckoo_exists_in_segment(self, seg_idx: int, tag: bytes) -> bool
```

Check if fingerprint exists in a segment.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `seg_idx` | int | Segment index |
| `tag` | bytes | Tag to check |

#### Returns

| Type | Description |
|------|-------------|
| bool | `True` if fingerprint exists, `False` otherwise |

---

### cuckoo_add_to_segment()

```python
def cuckoo_add_to_segment(self, seg_idx: int, tag: bytes) -> bool
```

Add fingerprint to a segment.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `seg_idx` | int | Segment index |
| `tag` | bytes | Tag to add |

#### Returns

| Type | Description |
|------|-------------|
| bool | `True` if duplicate found, `False` otherwise |

---

### cuckoo_rotate()

```python
def cuckoo_rotate(self) -> None
```

Rotate to next segment and clear it.

---

### cuckoo_is_segment_full()

```python
def cuckoo_is_segment_full(self, seg_idx: int) -> bool
```

Check if a segment is nearly full.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `seg_idx` | int | Segment index |

#### Returns

| Type | Description |
|------|-------------|
| bool | `True` if segment is > 95% full |

---

## Examples

### Basic Usage

```python
from src.try_26 import ASA_Crypt

# Create crypt instance
crypt = ASA_Crypt(b'my-key')

# Encrypt
encrypted = crypt.encrypt("Secret message")

# Decrypt
decrypted = crypt.decrypt(encrypted)
print(decrypted)  # "Secret message"
```

### Custom Configuration

```python
crypt = ASA_Crypt(
    key=b'my-secret-key',
    salt_size=32,
    nonce_size=24,
    hmac_size=32,
    block_size=64,
    cuckoo_num_segments=8,
    cuckoo_bucket_count=512,
    cuckoo_fingerprint_bits=16
)
```

### With Replay Protection

```python
crypt = ASA_Crypt(b'my-key')

# First encryption
msg1 = crypt.encrypt("One-time message")
print(crypt.decrypt(msg1))  # Works

# Replay attack
msg2 = crypt.decrypt(msg1)  # Returns None
print(msg2)  # None
```

### Checking Statistics

```python
crypt = ASA_Crypt(b'my-key')

# Encrypt many messages
for i in range(100):
    msg = crypt.encrypt(f"Message {i}")
    crypt.decrypt(msg)

# Check stats
print(f"Total checks: {crypt.cuckoo_total_checks}")
print(f"Replays detected: {crypt.cuckoo_detected}")
```

---

## Error Handling

All methods return `None` on error instead of raising exceptions:

```python
encrypted = crypt.encrypt("test")  # Returns str or None
if encrypted is None:
    print("Encryption failed")

decrypted = crypt.decrypt("invalid")  # Returns str or None
if decrypted is None:
    print("Decryption failed")
```

---

## Security Notes

### Key Management
- Use cryptographically random keys (32+ bytes)
- Never hardcode keys in source code
- Use environment variables or secure key management

### Salt and Nonce
- Automatically generated securely
- Should be unique for each encryption
- Included in the ciphertext

### Replay Protection
- Cuckoo filter with 12-bit fingerprints
- False positive rate: ~0.01%
- Auto-rotation prevents memory exhaustion

---

## Performance

### Benchmark Results (try_26)
- **Speed**: ~0.204ms per operation
- **Memory**: ~16KB for 4 segments
- **False Positive Rate**: ~0.01%

### Configuration Impact

| Parameter | Effect on Performance |
|-----------|----------------------|
| `cuckoo_num_segments` | More segments = slower |
| `cuckoo_bucket_count` | More buckets = slower |
| `cuckoo_fingerprint_bits` | More bits = slightly slower |

---

## References

- [Cuckoo Filter Paper](https://www.cs.cmu.edu/~dga/papers/cuckoo-conext2014.pdf)
- [Blake2 Specification](https://www.blake2.net/)
- [HMAC Standard](https://datatracker.ietf.org/doc/html/rfc2104)
```

---
