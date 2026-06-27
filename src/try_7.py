"""
try7: XOR + Salt + PBKDF2
--------------------------
Concept: Adding salt, using PBKDF2 to derive key
Security: VERY LOW - Better key derivation but still no authentication
Author: Amirsam Azmoodeh
"""

import hashlib
import base64
import zlib
import os

def encrypt(data , key) :
    salt = os.urandom(16)
    result = bytearray()
    key = hashlib.pbkdf2_hmac('sha256', key.encode(), salt, 600000, 32)
    compressed = zlib.compress(data.encode('utf-8'))

    for i , byt in enumerate(compressed) :
        k = key[i % len(key)]
        result.append(k ^ byt)

    return base64.b64encode(salt + result).decode('ascii')

 
def decrypt(data , key) :
    data = base64.b64decode(data)
    result = bytearray()
    salt = data[:16]
    data = data[16:]

    key = hashlib.pbkdf2_hmac('sha256', key.encode(), salt, 600000, 32)

    for i , byt in enumerate(data) :
        k = key[i % len(key)]
        result.append(byt ^ k)

    original_bytes = zlib.decompress(result)
    return original_bytes.decode('utf-8')
    

# Example usage
print(encrypt('this is one test!' , 'amirsam') )
print(decrypt('slQWoSa8qb0WTHhMx29o6GuGqWDIpf0e1eEpTC8DZrxT196cgFCOsfg=' , 'amirsam'))