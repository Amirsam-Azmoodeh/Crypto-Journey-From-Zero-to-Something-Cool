"""
try9: Stream Cipher with Counter
---------------------------------
Concept: Removed compression (security issue), added block counter
Security: LOW - Better keystream generation
Author: Amirsam Azmoodeh
"""

import hashlib
import base64
import os

def encrypt(data , key) :
    salt = os.urandom(16)
    nonce = os.urandom(16)
    result = bytearray()
    state = hashlib.pbkdf2_hmac('sha256', key.encode(), salt, 600000, 32)
    keystream = hashlib.sha256(state + hashlib.sha256(nonce + state).digest()).digest()
    data = data.encode('utf-8')
    
    counter = 0
    block_counter = 0

    for byt in data :
        if counter == 32:
            block_counter += 1
            keystream = hashlib.sha256(keystream + nonce + block_counter.to_bytes(8,'big')).digest()
            counter = 0

        c = keystream[counter] ^ byt
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
    keystream = hashlib.sha256(state + hashlib.sha256(nonce + state).digest()).digest()

    counter = 0
    block_counter = 0
    for byt in data :
        if counter == 32:
            block_counter += 1
            keystream = hashlib.sha256(keystream + nonce + block_counter.to_bytes(8,'big')).digest()
            counter = 0

        c = byt ^ keystream[counter]
        result.append(c)
        counter += 1

    return result.decode('utf-8')
    

# Example usage
print(encrypt('this is one test!' , 'amirsam') )