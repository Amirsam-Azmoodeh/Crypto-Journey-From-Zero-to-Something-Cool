"""
try2: Sequential Multiplication
-------------------------------
Concept: Cycle through key chars and multiply with data chars
Security: VERY LOW - Easy to break with frequency analysis
Author: Amirsam Azmoodeh
"""

def encrypt(data , key) :
    """Encrypt by multiplying each character with corresponding key character cyclically"""
    new_data = []

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
    """Decrypt by dividing each number by corresponding key character cyclically"""
    new_data = []

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
print(decrypt('11252.11336.11025.13110.3680.10185.12535.3104.12099.11550.11514.3680.11252.11009.11155.12644.3465' , 'amirsam'))