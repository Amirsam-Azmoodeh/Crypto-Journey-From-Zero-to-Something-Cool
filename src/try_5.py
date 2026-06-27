"""
try5: Optimized XOR + Hex
--------------------------
Concept: Use bytearray + hex output for efficiency
Security: VERY LOW - Same security as try4, just optimized
Author: Amirsam Azmoodeh
"""

import hashlib

def encrypt(data , key) :
    """Encrypt using XOR with bytearray (more efficient than list)"""
    new_data = bytearray()
    
    key = hashlib.sha256(key.encode()).digest()

    for i , char in enumerate(data) :
        k = key[i % len(key)]
        new_data.append(k ^ ord(char))

    return new_data.hex()

 
def decrypt(data , key) :
    """Decrypt using XOR with bytearray"""
    new_data = []
    
    key = hashlib.sha256(key.encode()).digest()

    data = bytes.fromhex(data)

    for i , char in enumerate(data) :
        k = key[i % len(key)]
        new_data.append(chr(char ^ k))

    return ''.join(new_data)
    

# Example usage
print(encrypt('this is one test!' , 'amirsam') )
print(decrypt('822be2484210aa468e061aa8b7af562590' , 'amirsam'))