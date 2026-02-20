# 🚀 Crypto Journey: From Zero to Something Cool!

<div align="center">
  
![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Learning%20Project-orange.svg)
![Age](https://img.shields.io/badge/Age-15%20years-purple.svg)

</div>

---

## 👋 Hey There! I'm Amirsam

<div align="center">
  
**15 years old | Programmer | Cryptography Enthusiast | From Iran 🇮🇷**

[![Email](https://img.shields.io/badge/Email-amirsamazmoodeh%40gmail.com-red?style=flat&logo=gmail)](mailto:amirsamazmoodeh@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Amirsam%20Azmoodeh-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/amirsam-azmoodeh)
[![GitHub](https://img.shields.io/badge/GitHub-@Amirsam--Azmoodeh-black?style=flat&logo=github)](https://github.com/Amirsam-Azmoodeh)

</div>

---

## 📖 About This Project

This repository documents my **personal learning journey** through the fascinating world of cryptography. I started with **zero knowledge** and built **7 different versions** of an encryption algorithm, learning something new with each iteration.

### 🎯 Why Did I Create This?

- To understand how encryption really works under the hood
- To learn from my mistakes (and there were MANY!)
- To share my journey with other young programmers
- To show that **learning is a process** - nobody becomes an expert overnight!

---

## 🗺️ The 7 Versions: My Learning Path

| Version | Name | Concept | My Learning |
|---------|------|---------|-------------|
| **v1** | [`Basic Sum`](v1_basic_sum.py) | Adding ASCII codes | ❌ Keys shouldn't be simplified! |
| **v2** | [`Sequential Mult`](v2_sequential_mult.py) | Cycling through key | ✅ Use entire key, ❌ Multiplication is weak |
| **v3** | [`SHA256 Hash`](v3_sha256_hash.py) | Hashing the key | ✅ Hash functions are useful, ❌ Hex isn't bytes |
| **v4** | [`Basic XOR`](v4_xor_basic.py) | XOR operation | 🔥 **XOR IS MAGIC!** (but still not enough) |
| **v5** | [`Optimized XOR`](v5_xor_optimized.py) | Bytearray + hex | ✅ Memory optimization matters |
| **v6** | [`XOR + Compression`](v6_xor_compressed.py) | zlib + Base64 | ✅ Compression = smaller output |
| **v7** | [`Salted PBKDF2`](v7_xor_salted_pbkdf2.py) | Salt + Key derivation | ✅ Professional concepts, ❌ Still not production-ready |

---

📊 Visual Comparison
text

Security Level (1-10):
v1:  ⭐········· (1/10)
v2:  ⭐⭐········ (2/10)
v3:  ⭐⭐········ (2/10)
v4:  ⭐⭐⭐······· (3/10)
v5:  ⭐⭐⭐······· (3/10)
v6:  ⭐⭐⭐⭐······ (4/10)
v7:  ⭐⭐⭐⭐⭐⭐···· (6/10)
AES: ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ (10/10)

Speed (Higher is Faster):
v1:  ██████████ (Lightning)
v7:  ████······ (Slower - PBKDF2)

🔬 Deep Dive: What I Learned at Each Step
🐣 Version 1: The Naive Beginning
python

new_key = sum(ord(i) for i in key)  # ❌ What was I thinking?!

Lesson: A key is NOT just a number! This can be cracked in milliseconds.
🐥 Version 2-3: Getting Better
python

# Cycling through key - Good!
# But multiplication - Still Bad!

Lesson: Using the whole key is important, but the operation matters too.
🦅 Version 4: The XOR Revelation
python

result = key_byte ^ data_byte  # ✨ MAGIC!

Lesson: XOR is the foundation of modern encryption. Perfectly reversible!
🦸 Version 7: Almost Professional
python

salt = os.urandom(16)
key = hashlib.pbkdf2_hmac('sha256', key.encode(), salt, 600000, 32)

Lesson: Salt prevents pattern recognition, PBKDF2 stops brute force!
⚠️ IMPORTANT WARNING
<div align="center">
🛑 DO NOT USE THIS IN PRODUCTION! 🛑
</div>

This code is for LEARNING ONLY. It has serious security flaws:
Problem	Why It's Dangerous
No Authentication	Anyone can modify encrypted data without detection
No Integrity Check	Can't verify if data was tampered with
Homemade Algorithm	Not tested by security experts
Vulnerable to Attacks	Bit-flipping, known-plaintext, etc.
✅ For Real Projects, Use:
python

from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()
f = Fernet(key)

# Encrypt securely
encrypted = f.encrypt(b"Secret message")

# Decrypt
decrypted = f.decrypt(encrypted)  # Raises error if tampered!

📚 What's Inside Each File?
File	What It Does
v1_basic_sum.py	My first attempt - sums key ASCII codes
v2_sequential_mult.py	Cycles through key with multiplication
v3_sha256_hash.py	Uses SHA256 hash of key
v4_xor_basic.py	First XOR implementation
v5_xor_optimized.py	Optimized with bytearray
v6_xor_compressed.py	Adds compression + Base64
v7_xor_salted_pbkdf2.py	Professional features: salt, PBKDF2
docs/evolution.md	Detailed story of my learning
docs/security_analysis.md	Complete security analysis

🤝 Want to Contribute?

I'd love your help! Here's how:

    🐛 Found a bug? Open an issue

    💡 Have an idea for v8? Create a pull request!

    📝 Found a mistake in my analysis? Let me know!

    🌍 Want to translate? Add your language version!

Guidelines:

    Keep the educational purpose

    Explain what you learned in your contribution

📬 Connect With Me

I'm always happy to chat with fellow programmers! Whether you're 15 or 50, beginner or expert:
<div align="center">
Platform	Link
📧 Email	amirsamazmoodeh@gmail.com
🔗 LinkedIn	Amirsam Azmoodeh
🐙 GitHub	@Amirsam-Azmoodeh
📍 Location	Iran 🇮🇷
</div>
📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
Feel free to use it for learning, but remember: not for production!
🌟 Star History

If you found this useful or learned something, please give it a ⭐! It helps other young programmers find it too.
<div align="center">
"The only way to learn is to make mistakes and understand why they're mistakes."

Made with ❤️ by a 15-year-old who loves cryptography
Amirsam Azmoodeh - 2026

⬆ Back to top
</div> ```