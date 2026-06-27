"""
try3: SHA256 + Multiplication
------------------------------
Concept: Hash key with SHA256, then multiply with data
Security: VERY LOW - Still vulnerable to statistical attacks
Author: Amirsam Azmoodeh
"""

import hashlib

def encrypt(data , key) :
    """Encrypt using SHA256 hashed key multiplied with data"""
    new_data = []
    
    key = str(hashlib.sha256(key.encode()).hexdigest())
    
    counter = 0
    counter2 = 0
    while counter2 < len(data) :

        if len(key) <= counter :
            counter = 0
        
        new_data.append(str(ord(key[counter]) * ord(data[counter2])))
        
        counter += 1
        counter2 += 1

    return '.'.join(new_data)

 
def decrypt(data , key) :
    """Decrypt by dividing each number by SHA256 hashed key"""
    new_data = []
    
    key = str(hashlib.sha256(key.encode()).hexdigest())
    
    counter = 0
    counter2 = 0

    data = data.split('.')
    while counter2 < len(data) :

        if len(key) <= counter :
            counter = 0
        
        new_data.append(chr(int(data[counter2]) // ord(key[counter])))
        
        counter += 1
        counter2 += 1

    return ''.join(new_data)
    

# Example usage
print(encrypt('this is one test!' , 'amirsam') )
print(decrypt('11832.5616.5460.5865.1792.10290.5865.3136.5994.5500.5555.1824.11600.5757.6210.6264.3333' , 'amirsam'))