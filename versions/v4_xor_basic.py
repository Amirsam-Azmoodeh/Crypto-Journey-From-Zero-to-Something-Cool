'''
Version 4: Basic XOR
-------------------
Concept: XOR data with hashed key (real breakthrough!)
Security: ⭐⭐⭐ MEDIUM (Educational only)
Author: Amirsam Azmoodeh (15, Iran)
'''


import hashlib

def encrypt(data , key) :
    new_data = []
    key = hashlib.sha256(key.encode()).digest() # Get real bytes (not hex!)
    counter = 0
    counter2 = 0
    while counter2 < len(data) :

        if len(key)  <= counter :
            counter = 0
        
        new_data.append(str(key[counter] ^ ord(data[counter2]))) # XOR operation
        
        counter += 1
        counter2 += 1

    return '.'.join(new_data)

 
def decrypt(data , key) :
    new_data = []
    key = hashlib.sha256(key.encode()).digest()
    counter = 0
    counter2 = 0

    data = data.split('.')
    while counter2 < len(data) :

        if len(key) <= counter :
            counter = 0
        
        new_data.append(chr(int(data[counter2]) ^  key[counter])) # Reverse XOR
        
        counter += 1
        counter2 += 1

    return ''.join(new_data)
    

print(encrypt('this is one test!' , 'amirsam') )
print(decrypt('130.43.226.72.66.16.170.70.142.6.26.168.183.175.86.37.144' , 'amirsam'))
