# 🧬 Evolution of Code: From Zero to Something Cool!

## 👋 About This Journey
Hi! I'm **Amirsam Azmoodeh**, a 15-year-old programmer from Iran. This repository documents my learning journey through the fascinating world of cryptography. I started with zero knowledge and built 7 different versions of an encryption algorithm, learning something new with each iteration.

---

## 📊 Version Comparison Table

| Version | Core Concept | Security Level | Speed | Lines of Code | What I Learned |
|---------|--------------|----------------|--------|---------------|----------------|
| [v1](v1_basic_sum.py) | Simple ASCII Sum | ⭐ Very Low | ⚡ Lightning | 15 | Basic encryption concept |
| [v2](v2_sequential_mult.py) | Sequential Multiplication | ⭐ Low | ⚡ Lightning | 20 | Key cycling importance |
| [v3](v3_sha256_hash.py) | SHA256 Hashing | ⭐⭐ Low-Medium | ⚡ Fast | 25 | Hash functions |
| [v4](v4_xor_basic.py) | Basic XOR | ⭐⭐ Medium | ⚡ Fast | 25 | XOR magic |
| [v5](v5_xor_optimized.py) | Optimized XOR | ⭐⭐ Medium | ⚡ Faster | 20 | Bytearray & memory optimization |
| [v6](v6_xor_compressed.py) | XOR + Compression | ⭐⭐ Medium | ⚡ Fast | 25 | Compression benefits |
| [v7](v7_xor_salted_pbkdf2.py) | Salt + PBKDF2 | ⭐⭐⭐ High | 🐢 Slower | 35 | Salt & key derivation |

---

## 🗺️ Detailed Evolution Path

### Version 1: The Beginning
```python
new_key = sum(ord(i) for i in key)
new_data = [str(ord(i) * new_key) for i in data]

What I learned: This was my first attempt! I realized that converting the whole key to a single number is very weak. The same input always produces the same output.

Mistake: Using addition and multiplication instead of real cryptographic operations.
Version 2: Getting Sequential
python

while counter2 < len(data):
    if len(key) <= counter:
        counter = 0
    new_data.append(str(ord(key[counter]) * ord(data[counter2])))

Improvement: Now each character uses a different part of the key cyclically!

What I learned: The importance of using the entire key, not just a summary of it.

Still wrong: Multiplication is reversible and patterns emerge.
Version 3: Introducing Hashing
python

key = str(hashlib.sha256(key.encode()).hexdigest())

Improvement: Using SHA256 to get a fixed-length key!

What I learned: Hash functions can turn any input into a consistent length.

Problem: I was still using hex digits as strings, not real bytes.
Version 4: The XOR Revelation
python

new_data.append(str(key[counter] ^ ord(data[counter2])))

BREAKTHROUGH MOMENT! This is when I discovered XOR!

What I learned: XOR is the foundation of modern encryption. It's reversible and perfect for cryptography.

Still missing: My output was still numbers with dots.
Version 5: Optimization & Bytes
python

new_data = bytearray()
for i, char in enumerate(data):
    k = key[i % len(key)]
    new_data.append(k ^ ord(char))
return new_data.hex()

Improvement: Using bytearray and enumerate made the code cleaner and faster!

What I learned: Working directly with bytes is more efficient than strings.
Version 6: Compression Magic
python

compressed = zlib.compress(data.encode('utf-8'))
# ... XOR operations ...
return base64.b64encode(new_data).decode('ascii')

Improvement: Added compression and Base64 output!

What I learned: Compression before encryption is smart - smaller data, faster processing. Base64 makes output readable.
Version 7: Professional Touch
python

salt = os.urandom(16)
key = hashlib.pbkdf2_hmac('sha256', key.encode(), salt, 600000, 32)

Final Evolution: Added salt and PBKDF2!

What I learned:

    Salt makes the same text produce different ciphertext each time

    PBKDF2 makes brute-force attacks impractical

    Key derivation functions are essential for security

🌟 Final Thought

This journey taught me that cryptography is like a puzzle - every piece must fit perfectly. One small mistake can break everything. That's why we trust algorithms tested by thousands of experts over decades.

Thanks for checking out my learning journey! 🚀

*— Amirsam Azmoodeh, 15-year-old programmer from Iran*
📧 amirsamazmoodeh@gmail.com
🔗 www.linkedin.com/in/amirsam-azmoodeh
🐙 https://github.com/Amirsam-Azmoodeh





