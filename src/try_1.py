"""
try1: Basic Sum Encryption
---------------------------
Concept: Sum all ASCII codes of key and multiply with each character
Security: VERY LOW - Educational only, not for real use
Author: Amirsam Azmoodeh
"""

def encrypt(data , key) :
    """Encrypt data by multiplying each character with sum of key's ASCII values"""
    
    new_key = 0
    for i in key :
        new_key += ord(i)

    new_data = []

    for i in data :
        new_data.append(str(ord(i) * new_key))

    return '.'.join(new_data)

 
def decrypt(data , key) :
    """Decrypt by dividing each number by sum of key's ASCII values"""
    
    new_key = 0
    for i in key :
        new_key += ord(i)

    new_data = []

    data = data.split('.')

    for i in data :
        new_data.append(chr(int(i) // new_key))

    return ''.join(new_data)
    

# Example usage
print(encrypt('this is one test!' , 'amirsam') )
print(decrypt('86536.77584.78330.85790.23872.78330.85790.23872.82806.82060.75346.23872.86536.75346.85790.86536.24618' , 'amirsam'))