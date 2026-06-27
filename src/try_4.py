"""
try4: Basic XOR
----------------
Concept: XOR data with hashed key bytes
Security: VERY LOW - Better but still vulnerable
Author: Amirsam Azmoodeh
"""

import hashlib

def encrypt(data , key) :
    """Encrypt using XOR with SHA256 key bytes"""
    new_data = []
    
    key = hashlib.sha256(key.encode()).digest()
    
    counter = 0
    counter2 = 0
    while counter2 < len(data) :

        if len(key) <= counter :
            counter = 0
        
        new_data.append(str(key[counter] ^ ord(data[counter2])))
        
        counter += 1
        counter2 += 1

    return '.'.join(new_data)

 
def decrypt(data , key) :
    """Decrypt using XOR with SHA256 key bytes"""
    new_data = []
    
    key = hashlib.sha256(key.encode()).digest()
    
    counter = 0
    counter2 = 0

    data = data.split('.')
    while counter2 < len(data) :

        if len(key) <= counter :
            counter = 0
        
        new_data.append(chr(int(data[counter2]) ^ key[counter]))
        
        counter += 1
        counter2 += 1

    return ''.join(new_data)
    

# Example usage
print(encrypt('this is one test!' , 'amirsam') )
print(decrypt('130.43.226.72.66.16.170.70.142.6.26.168.183.175.86.37.144' , 'amirsam'))