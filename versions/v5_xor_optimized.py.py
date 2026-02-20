'''
Version 5: Optimized XOR + Hex
------------------------------
Concept: Use bytearray + hex output for efficiency
Security: ⭐⭐⭐ MEDIUM (Educational only)
Author: Amirsam Azmoodeh (15, Iran)
'''


import hashlib

def encrypt(data , key) :
    new_data = bytearray() # More efficient than list
    key = hashlib.sha256(key.encode()).digest()

    for i , char in enumerate(data) :

        k = key[i % len(key)]
        new_data.append(k ^ ord(char)) # XOR and store as bytes
  

    return new_data.hex()  # Hex output (no dots!)
 

def decrypt(data , key) :
    new_data = []
    key = hashlib.sha256(key.encode()).digest()

    data = bytes.fromhex(data) # Convert hex back to bytes

    for i , char in enumerate(data) :

        k = key[i % len(key)]
        new_data.append(chr(char ^  k))


    return ''.join(new_data)
    

print(encrypt('this is one test!' , 'amirsam') )
print(decrypt('822be2484210aa468e061aa8b7af562590' , 'amirsam'))
