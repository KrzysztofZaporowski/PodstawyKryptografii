import sympy
import secrets

def generate_keys(value):
    p = sympy.randprime(10**value, 10**(value + 1))
    q = sympy.randprime(10**value, 10**(value + 1))

    while q == p:
        q = sympy.randprime(10**value, 10**(value + 1))

    phi = (p - 1) * (q - 1)

    e = secrets.randbelow(phi - 1) + 1
    while sympy.gcd(e, phi) != 1:
        e = secrets.randbelow(phi - 1) + 1
    
    d = sympy.mod_inverse(e, phi)