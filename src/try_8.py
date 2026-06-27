"""
try8: XOR + Salt + PBKDF2 + Nonce
----------------------------------
Concept: Added nonce to prevent pattern recognition
Security: VERY LOW - Better but still no authentication
Author: Amirsam Azmoodeh
"""

import hashlib
import base64
import zlib
import os

def encrypt(data , key) :
    salt = os.urandom(16)
    nonce = os.urandom(16)
    result = bytearray()
    state = hashlib.pbkdf2_hmac('sha256', key.encode(), salt, 600000, 32)
    compressed = zlib.compress(data.encode('utf-8'))

    counter = 0

    for byt in compressed :
        if counter == 32:
            state = hashlib.sha256(state + nonce).digest()
            counter = 0

        c = state[counter] ^ byt
        result.append(c)
        counter += 1

    return base64.b64encode(salt + nonce + bytes(result)).decode('ascii')

 
def decrypt(data , key) :
    data = base64.b64decode(data)
    result = bytearray()
    salt = data[:16]
    nonce = data[16:32]
    data = data[32:]

    state = hashlib.pbkdf2_hmac('sha256', key.encode(), salt, 600000, 32)
    
    counter = 0

    for byt in data :
        if counter == 32:
            state = hashlib.sha256(state + nonce).digest()
            counter = 0

        c = byt ^ state[counter]
        result.append(c)
        counter += 1

    original_bytes = zlib.decompress(result)
    return original_bytes.decode('utf-8')
    

# Example usage
print(encrypt('this is one test!' , 'amirsam') )
print(decrypt('a+11VJtAbWRKOwLCD3hWRFG0JwsSpVAqgA559RpfEx62QnRk9xLnFhm1q5GSSMVl7l+6qTTmVdzL' , 'amirsam'))