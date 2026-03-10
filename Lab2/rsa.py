import sympy
import secrets
import sys

def generate_keys():
    p = sympy.randprime(1000, 10000)
    q = sympy.randprime(1000, 10000)

    while q == p:
        q = sympy.randprime(1000, 10000)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = secrets.randbelow(phi - 1) + 1
    while sympy.gcd(e, phi) != 1:
        e = secrets.randbelow(phi - 1) + 1
    
    d = sympy.mod_inverse(e, phi)

    return (e, n), (d, n)

def encrypt(message, public_key):
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in message]
    return cipher

def decrypt(cipher, private_key):
    d, n = private_key
    message = ''.join([chr(pow(char, d, n)) for char in cipher])
    return message

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python rsa.py <message>")
        sys.exit(1)
        
    public_key, private_key = generate_keys()
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")

    message = sys.argv[1]
    print(f"Original Message: {message}")

    cipher = encrypt(message, public_key)
    print(f"Encrypted Message: {cipher}")

    decrypted_message = decrypt(cipher, private_key)
    print(f"Decrypted Message: {decrypted_message}")