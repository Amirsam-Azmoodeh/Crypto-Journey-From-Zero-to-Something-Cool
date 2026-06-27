"""
try6: XOR + Compression + Base64
---------------------------------
Concept: Compress before encrypt, use Base64 output
Security: VERY LOW - Compression adds no real security
Author: Amirsam Azmoodeh
"""

import hashlib
import base64
import zlib

def encrypt(data , key) :
    new_data = bytearray()
    key = hashlib.sha256(key.encode()).digest()
    compressed = zlib.compress(data.encode('utf-8'))

    for i , byt in enumerate(compressed) :
        k = key[i % len(key)]
        new_data.append(k ^ byt)

    return base64.b64encode(new_data).decode('ascii')

 
def decrypt(data , key) :
    new_data = bytearray()
    key = hashlib.sha256(key.encode()).digest()

    data = base64.b64decode(data)

    for i , byt in enumerate(data) :
        k = key[i % len(key)]
        new_data.append(byt ^ k)

    original_bytes = zlib.decompress(new_data)
    return original_bytes.decode('utf-8')
    

# Example usage
print(encrypt('this is one test!' , 'amirsam') )
print(decrypt('jt+g8qpVj67NPrdHiJ8NGJxN823wcNOo6w==' , 'amirsam'))