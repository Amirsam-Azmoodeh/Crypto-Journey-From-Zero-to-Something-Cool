'''
Version 6: XOR + Compression + Base64
------------------------------------
Concept: Compress before encrypt, use Base64 output
Security: ⭐⭐⭐⭐ MEDIUM-HIGH (Educational only)
Author: Amirsam Azmoodeh (15, Iran)
'''


import hashlib
import base64
import zlib

def encrypt(data , key) :
    new_data = bytearray()
    key = hashlib.sha256(key.encode()).digest()
    compressed = zlib.compress(data.encode('utf-8')) # Compress first

    for i , byt in enumerate(compressed) :

        k = key[i % len(key)]
        new_data.append(k ^ byt) # XOR with bytes
  

    return base64.b64encode(new_data).decode('ascii') # Base64 output
 

def decrypt(data , key) :
    new_data = bytearray()
    key = hashlib.sha256(key.encode()).digest()

    data = base64.b64decode(data) # Decode Base64

    for i , byt in enumerate(data) :

        k = key[i % len(key)]
        new_data.append(byt ^  k)

    original_bytes = zlib.decompress(new_data) # Decompress
    return original_bytes.decode('utf-8')
    

print(encrypt('this is one test!' , 'amirsam') )
print(decrypt('jt+g8qpVj67NPrdHiJ8NGJxN823wcNOo6w==' , 'amirsam'))
