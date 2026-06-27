
```markdown
# 🚀 Quick Start Guide

## 5 Minutes to Your First Encryption

This guide will help you get started with Crypto-Journey in just 5 minutes!

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/crypto-journey.git
cd crypto-journey
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Your First Encryption

### Basic Usage

```python
from src.try_26 import ASA_Crypt

# Create crypt instance
crypt = ASA_Crypt(b'my-secret-key')

# Encrypt a message
plaintext = "Hello, World!"
encrypted = crypt.encrypt(plaintext)
print(f"🔒 Encrypted: {encrypted}")

# Decrypt the message
decrypted = crypt.decrypt(encrypted)
print(f"🔓 Decrypted: {decrypted}")
```

**Expected Output:**
```
🔒 Encrypted: EhIMAQAA4vLeOVHh9Yws1oC3vHw/bi...
🔓 Decrypted: Hello, World!
```

---

## 🛡️ Replay Protection Demo

```python
from src.try_26 import ASA_Crypt

crypt = ASA_Crypt(b'my-key')

# Encrypt a one-time message
msg = crypt.encrypt("This is a one-time message")

# First decryption - works!
result1 = crypt.decrypt(msg)
print(f"✅ First: {result1}")

# Second decryption - blocked!
result2 = crypt.decrypt(msg)
print(f"❌ Replay: {result2}")
```

**Expected Output:**
```
✅ First: This is a one-time message
❌ Replay: None
```

---

## ⚙️ Custom Configuration

```python
from src.try_26 import ASA_Crypt

# High security configuration
crypt = ASA_Crypt(
    key=b'my-secret-key',
    salt_size=32,              # Larger salt
    nonce_size=24,             # Larger nonce
    hmac_size=32,              # Full HMAC
    cuckoo_num_segments=8,     # More segments
    cuckoo_bucket_count=1024,  # More buckets
    cuckoo_fingerprint_bits=16 # More fingerprint bits
)

encrypted = crypt.encrypt("Secure message")
decrypted = crypt.decrypt(encrypted)
print(decrypted)  # Secure message
```

---

## 📊 Check Statistics

```python
from src.try_26 import ASA_Crypt

crypt = ASA_Crypt(b'my-key')

# Send some messages
for i in range(100):
    msg = crypt.encrypt(f"Message {i}")
    crypt.decrypt(msg)

# Check stats
print(f"Total checks: {crypt.cuckoo_total_checks}")
print(f"Replays detected: {crypt.cuckoo_detected}")
```

---

## 🔄 Compare Versions

```python
from src.try_5 import encrypt as encrypt_v5, decrypt as decrypt_v5
from src.try_26 import ASA_Crypt

# Version 5 - Fast but insecure
encrypted_v5 = encrypt_v5("Hello", "key")
decrypted_v5 = decrypt_v5(encrypted_v5, "key")

# Version 26 - Secure but slower
crypt_v26 = ASA_Crypt(b'key')
encrypted_v26 = crypt_v26.encrypt("Hello")
decrypted_v26 = crypt_v26.decrypt(encrypted_v26)

print(f"V5: {decrypted_v5}")
print(f"V26: {decrypted_v26}")
```

---

## 🧪 Run Tests

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_try_26.py

# Run with coverage
pytest --cov=src tests/
```

---

## 📈 Run Benchmarks

```bash
# Fast benchmark (50 iterations)
python examples/benchmark_fast.py

# Full benchmark (500 iterations)
python examples/benchmark.py

# Compare versions
python examples/compare_versions.py
```

---

## 🎯 Common Use Cases

### 1. Encrypt a File

```python
from src.try_26 import ASA_Crypt

crypt = ASA_Crypt(b'my-key')

# Read file
with open('secret.txt', 'r') as f:
    content = f.read()

# Encrypt
encrypted = crypt.encrypt(content)

# Save encrypted
with open('secret.enc', 'w') as f:
    f.write(encrypted)
```

### 2. Decrypt a File

```python
from src.try_26 import ASA_Crypt

crypt = ASA_Crypt(b'my-key')

# Read encrypted file
with open('secret.enc', 'r') as f:
    encrypted = f.read()

# Decrypt
decrypted = crypt.decrypt(encrypted)

# Save decrypted
with open('secret_decrypted.txt', 'w') as f:
    f.write(decrypted)
```

### 3. Encrypt API Data

```python
from src.try_26 import ASA_Crypt
import json

crypt = ASA_Crypt(b'api-key')

data = {"user": "alice", "action": "login"}
json_data = json.dumps(data)

encrypted = crypt.encrypt(json_data)
# Send encrypted data to API
```

### 4. Secure Messaging

```python
from src.try_26 import ASA_Crypt

class SecureMessenger:
    def __init__(self, key):
        self.crypt = ASA_Crypt(key)
    
    def send(self, message):
        return self.crypt.encrypt(message)
    
    def receive(self, encrypted):
        return self.crypt.decrypt(encrypted)

# Usage
messenger = SecureMessenger(b'shared-secret')
encrypted = messenger.send("Hello, Alice!")
decrypted = messenger.receive(encrypted)
print(decrypted)  # Hello, Alice!
```

---

## 🐛 Troubleshooting

### Error: "maximum key length is 32 bytes"

**Solution**: Use a key of exactly 32 bytes:

```python
# Wrong
crypt = ASA_Crypt(b'key')  # Too short

# Correct
crypt = ASA_Crypt(b'key' * 8)  # 24 bytes (but still not 32)

# Best
crypt = ASA_Crypt(b'key' * 11)  # 33 bytes (too long)

# Perfect
crypt = ASA_Crypt(b'key' * 10 + b'01')  # Exactly 32 bytes
```

### Error: "bitarray not installed"

**Solution**:
```bash
pip install bitarray
```

### Error: "ModuleNotFoundError"

**Solution**: Make sure you're in the project root:
```bash
cd /path/to/crypto-journey
python -c "import src.try_26"
```

---

## 📚 Next Steps

1. **Read the [Evolution](evolution.md)** - Understand how each version evolved
2. **Check [Security Analysis](security_analysis.md)** - Learn about security trade-offs
3. **Explore [Cuckoo Filter](cuckoo_filter.md)** - Deep dive into replay protection
4. **Review [API Reference](api_reference.md)** - Complete documentation

---

## 💡 Tips

1. **Use environment variables for keys**:
   ```python
   import os
   key = os.environ.get('CRYPTO_KEY', b'default-key').encode()
   crypt = ASA_Crypt(key)
   ```

2. **Handle errors gracefully**:
   ```python
   result = crypt.decrypt(encrypted)
   if result is None:
       print("Decryption failed")
   else:
       print(result)
   ```

3. **Monitor performance**:
   ```python
   import time
   start = time.time()
   encrypted = crypt.encrypt("test")
   print(f"Took {time.time() - start:.3f}s")
   ```

---

## 🎉 Congratulations!

You've successfully started your crypto journey! Remember:

- ✅ This is for **learning**, not production
- ✅ Always use **well-audited libraries** in production
- ✅ **Security** takes time to learn

Happy coding! 🚀
```

---

## 📄 پیام ۶: docs/contributing_guide.md

```markdown
# 🤝 Contributing Guide

## Welcome!

Thank you for considering contributing to Crypto-Journey! This project is built for learning, and your contributions help make it better for everyone.

---

## 📋 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](../CODE_OF_CONDUCT.md). Please be respectful and inclusive.

---

## 🚀 How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please:
1. Check existing issues
2. Check if the bug is already fixed in the latest version

When reporting bugs, include:
- **Clear title** describing the issue
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Python version** (`python --version`)
- **Error messages** (full stack trace)

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When suggesting:

- **Clear title** describing the enhancement
- **Step-by-step** description of how it would work
- **Examples** of usage
- **Why it's useful**

### 🔧 Pull Requests

1. **Fork the repository**
2. **Create a branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Run tests**: `pytest tests/`
5. **Update documentation**
6. **Commit**: `git commit -m 'Add amazing feature'`
7. **Push**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

---

## 📝 Development Setup

### Prerequisites
- Python 3.8+
- Git

### Setup

```bash
# Clone your fork
git clone https://github.com/your-username/crypto-journey.git
cd crypto-journey

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

---

## 🧪 Testing

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test
```bash
pytest tests/test_try_26.py
pytest tests/test_cuckoo.py
```

### Run with Coverage
```bash
pytest --cov=src tests/
pytest --cov=src --cov-report=html tests/
```

### Test Structure

```python
# tests/test_new_feature.py
import pytest
from src.try_26 import ASA_Crypt

class TestNewFeature:
    @pytest.fixture
    def crypt(self):
        return ASA_Crypt(b'test-key')
    
    def test_encrypt_decrypt(self, crypt):
        plaintext = "Hello"
        encrypted = crypt.encrypt(plaintext)
        decrypted = crypt.decrypt(encrypted)
        assert decrypted == plaintext
    
    def test_error_handling(self, crypt):
        assert crypt.decrypt("invalid") is None
```

---

## 📝 Code Style

We follow these guidelines:

### PEP 8
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable names

### Type Hints

```python
def encrypt(self, plaintext: str) -> str:
    """Encrypt plaintext string."""
    # ...
```

### Docstrings (Google Style)

```python
def function_name(param1: type, param2: type) -> return_type:
    """Brief description of function.
    
    More detailed description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When this happens
    """
```

### Example

```python
def create_keystream(self, state: bytes, nonce: bytes, block_counter: int) -> bytes:
    """Generate keystream using Blake2b.
    
    This function creates a cryptographically secure keystream
    for XOR encryption/decryption.
    
    Args:
        state: Current encryption state (32 bytes)
        nonce: Nonce value for uniqueness
        block_counter: Current block counter
        
    Returns:
        Keystream bytes (64 bytes from Blake2b)
        
    Example:
        >>> crypt = ASA_Crypt(b'key')
        >>> keystream = crypt.create_keystream(state, nonce, 0)
        >>> len(keystream)
        64
    """
    return hashlib.blake2b(
        nonce + block_counter.to_bytes(8, 'big'),
        key=state,
        digest_size=64
    ).digest()
```

---

## 📚 Documentation

### Update README
- Keep it up to date with new features
- Add examples for new functionality

### Add Docstrings
- Every function should have a docstring
- Include examples for complex functions

### Update Examples
- Add examples for new features
- Keep examples working

### Documentation Files
- `docs/evolution.md` - Version history
- `docs/security_analysis.md` - Security analysis
- `docs/cuckoo_filter.md` - Cuckoo filter deep dive
- `docs/api_reference.md` - API documentation

---

## 🏷️ Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible new features
- **PATCH**: Backwards-compatible bug fixes

Example:
```
2.0.0 -> Major release (breaking changes)
1.5.0 -> Minor release (new feature)
1.4.3 -> Patch release (bug fix)
```

---

## 📊 Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

### Examples
```
feat: Add cuckoo filter for replay protection
fix: Correct Blake2s key length issue
docs: Update security analysis document
test: Add tests for cuckoo filter
refactor: Simplify encryption logic
```

---

## 🔍 Code Review Process

1. **Self-review** your code first
2. **Run tests** locally
3. **Update documentation**
4. **Create Pull Request**
5. **Address feedback** from reviewers
6. **Merge** when approved

### What Reviewers Check
- Code correctness
- Test coverage
- Documentation
- Security implications
- Performance impact
- Code style

---

## 🎯 Areas for Contribution

### Easy (Good First Issue)
- 📝 Improve documentation
- 🧪 Add test cases
- 🐛 Fix typos
- ✨ Add examples

### Medium
- 🔧 Add new features
- 🚀 Optimize performance
- 🔒 Improve security
- 📊 Add statistics

### Advanced
- 🦆 Enhance cuckoo filter
- 🔑 Add key exchange
- 🌐 Add network protocol
- 📦 Package for PyPI

---

## 📧 Questions?

- **Email**: amirsamazmoodeh@gmail.com
- **LinkedIn**: [Amirsam Azmoodeh](https://linkedin.com/in/amirsam-azmoodeh)
- **GitHub**: Open an issue

---

## 🙏 Thank You!

Your contributions make this project better for everyone learning cryptography!

**Happy Coding!** 🚀
```

```markdown
# ❓ Frequently Asked Questions

## General Questions

### Q: What is Crypto-Journey?

**A**: Crypto-Journey is an educational project that shows the evolution of a cryptographic system from very basic (try_1) to relatively secure (try_26). Each version adds new security features and fixes vulnerabilities from previous versions.

### Q: Can I use this in production?

**A**: **NO!** This is for educational purposes only. Always use well-audited libraries like `cryptography` or `libsodium` in production.

### Q: Why are there 26 versions?

**A**: Each version represents a step in the learning process. Starting from the simplest concept (try_1) and gradually adding features like authentication, key derivation, and replay protection.

### Q: Which version should I use?

**A**:
- **For learning**: Start with try_1 and work your way up
- **For best security**: Use try_26
- **For fastest speed**: Use try_5 (but it's insecure!)

---

## Technical Questions

### Q: Why is try_10 so slow?

**A**: try_10 uses PBKDF2 with 600,000 iterations. This is intentionally slow to prevent brute force attacks. In production, this is a good thing, but it makes benchmarks slow.

### Q: What's a cuckoo filter?

**A**: A cuckoo filter is a probabilistic data structure used for membership testing. It's used in try_25 and try_26 for replay protection. It has very low false positive rates (~0.01%) and supports deletion.

Learn more: [Cuckoo Filter Deep Dive](cuckoo_filter.md)

### Q: What's the difference between Blake2s and Blake2b?

**A**:
- **Blake2s**: 32-bit architecture, 32-byte output
- **Blake2b**: 64-bit architecture, 64-byte output
- Blake2b is faster on 64-bit systems

### Q: Why do I get "maximum key length is 32 bytes"?

**A**: Blake2s has a maximum key length of 32 bytes. You're passing a key longer than 32 bytes. Use exactly 32 bytes:

```python
# Wrong
crypt = ASA_Crypt(b'this_is_a_very_long_key_that_is_too_long')

# Correct
crypt = ASA_Crypt(b'this_is_32_bytes_long____')  # Exactly 32 bytes
```

### Q: What is a bitmap and why use it?

**A**: A bitmap is an array of bits used to track seen tags. It's very memory efficient (8KB for 65,536 bits) compared to a set (8MB for 65,536 entries).

### Q: What are false positives in replay protection?

**A**: A false positive is when the system incorrectly identifies a new message as a replay. This can happen with bitmaps (try_21) and cuckoo filters (try_25) but not with sets (try_19).

---

## Security Questions

### Q: Is try_26 secure?

**A**: For educational purposes, try_26 implements reasonable security:
- ✅ Authentication (HMAC)
- ✅ Replay protection (Cuckoo filter)
- ✅ Key derivation (HKDF-like)
- ✅ Modern algorithms (Blake2b)

**BUT**: It's still not production-ready. Use well-audited libraries.

### Q: What are the main security issues in early versions?

**A**:
- **try_1-6**: No authentication, deterministic
- **try_7-9**: No authentication
- **try_10-13**: Slow but still missing replay protection
- **try_18**: Critical bug (using dict instead of set)

### Q: What's the false positive rate of the cuckoo filter?

**A**: With default settings (12-bit fingerprints, bucket size 4):
```
P(false positive) ≈ 1 / (2^12) × 1/4 ≈ 0.006%
```

### Q: How does HMAC help security?

**A**: HMAC provides:
1. **Authentication**: Verifies message sender
2. **Integrity**: Detects tampering
3. **Non-repudiation**: Sender cannot deny sending

---

## Performance Questions

### Q: Which version is fastest?

**A**: try_5 (0.017ms) is the fastest, but it's insecure.

### Q: How do different versions compare in speed?

| Version | Time | Security |
|---------|------|----------|
| try_5 | 0.017ms | 🔴 VERY LOW |
| try_1 | 0.019ms | 🔴 VERY LOW |
| try_21 | 0.066ms | 🟡 MEDIUM-HIGH |
| try_19 | 0.067ms | 🟡 MEDIUM |
| try_15 | 0.079ms | 🟡 MEDIUM |
| try_23 | 0.083ms | 🟢 MEDIUM-HIGH |
| try_26 | 0.204ms | 🟢 HIGH |
| try_10 | 1.032ms | 🟡 LOW |

### Q: Why is try_10 so slow?

**A**: It uses PBKDF2 with 600,000 iterations. This is intentional to slow down brute force attacks.

### Q: How can I improve performance?

**A**:
1. Use smaller salt/nonce sizes
2. Reduce cuckoo filter segments
3. Use a smaller bitmap
4. Use try_5 if security isn't needed

---

## Code Questions

### Q: Why is `try_18` called "Buggy"?

**A**: try_18 uses `{}` (dict) instead of `set()`:
```python
self.ciphertext_set = {}  # ❌ This is a dict
```
This causes `AttributeError` when calling `.add()`.

### Q: What's the difference between try_19 and try_20?

**A**:
- **try_19**: Set with unlimited growth
- **try_20**: Set limited to 100 entries

try_20 prevents memory exhaustion but may miss replays after 100 messages.

### Q: How does auto-reset work in try_23?

**A**: When the bitmap reaches 80% usage, the oldest 33% of tags are cleared. This prevents false positives from building up.

### Q: Why use bitarray library?

**A**: `bitarray` provides efficient bit-level operations. For 65,536 bits:
- Python list: ~500KB
- `bitarray`: ~8KB

---

## Installation Questions

### Q: What Python version do I need?

**A**: Python 3.8 or higher.

### Q: How do I install dependencies?

**A**:
```bash
pip install -r requirements.txt
```

### Q: I get "ModuleNotFoundError: No module named 'bitarray'"

**A**:
```bash
pip install bitarray
```

### Q: I get "ModuleNotFoundError: No module named 'src'"

**A**: Make sure you're in the project root directory:
```bash
cd /path/to/crypto-journey
python examples/usage_example.py
```

---

## Contribution Questions

### Q: How can I contribute?

**A**: Check [Contributing Guide](contributing_guide.md). You can:
- Report bugs
- Suggest features
- Improve documentation
- Submit pull requests

### Q: What are good first issues?

**A**:
- Improve documentation
- Add test cases
- Fix typos
- Add examples

### Q: What should I include in my PR?

**A**:
- Clear description of changes
- Tests for new features
- Updated documentation
- Follow code style

---

## License Questions

### Q: What license is this project under?

**A**: Apache License 2.0

### Q: Can I use this code in my project?

**A**: Yes! Under the terms of the Apache 2.0 license:
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Sublicensing
- ❌ Liability
- ❌ Warranty

### Q: Do I need to include the license?

**A**: Yes, you must include the license text and copyright notice.

---

## Miscellaneous Questions

### Q: Where can I learn more about cryptography?

**A**:
- [Cryptography Engineering](https://www.schneier.com/books/cryptography_engineering/)
- [OWASP Cryptographic Storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [Python Cryptography](https://cryptography.io/)

### Q: What's the next step after this project?

**A**:
1. Use a well-audited library (`cryptography`, `libsodium`)
2. Learn about key exchange (Diffie-Hellman, ECDH)
3. Study TLS/SSL
4. Build a secure messaging app

### Q: Why the name "Crypto-Journey"?

**A**: Because it documents a journey from "I know nothing" to "I understand cryptographic concepts" through 26 steps of building and breaking encryption.

---

## 📬 Still Have Questions?

- **Email**: amirsamazmoodeh@gmail.com
- **GitHub**: Open an issue
- **LinkedIn**: [Amirsam Azmoodeh](https://linkedin.com/in/amirsam-azmoodeh)

---

**Happy Learning!** 🚀
```

---
