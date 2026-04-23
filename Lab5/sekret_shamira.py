import random
import sympy
import secrets

# n - liczba wszystkich udziałów
# t - liczba udziałów potrzebna do rekonstrukcji sekretu
# s - sekret do podziału
# k - wartość liczbowa określająca przestrzeń liczbową


def modInverse(a, p):
    # Obliczanie odwrotności modularnej: a^(-1) mod p
    return pow(a, p - 2, p)

def trivial_secret_sharing(n, s):
    # Podział sekretu
    k = random.choice(range(s+1, 3 * s + 1))
    s_list = []
    for _ in range(n - 1):
        print(_)
        s_list.append(secrets.randbelow(k))

    s_n = (s - sum(s_list)) % k
    s_list.append(s_n)

    print(f"Udziały: {s_list}")
    print(f"Sekret: {s}")

    return s_list, k

def trivial_secret_reconstruction(shares, k):
    # Rekonstrukcja sekretu
    s = sum(shares) % k
    print(f"Rekonstruowany sekret: {s}")

    return s

def shamir_secret_sharing(n, t, s, p=None):
    # Podział sekretu Shamir
    if p is not None and p <= max(s, n):
        raise ValueError("Moduł p musi być większy niż maksymalna wartość sekretu i liczba udziałów.")
    if sympy.isprime(p) is False:
        raise ValueError("Moduł p musi być liczbą pierwszą.")
    if p is None:
        p = sympy.nextprime(max(s, n))
    a_s = []
    for _ in range(t - 1):
        a_s.append(random.choice(range(0, p - 1)))
    s_list = []

    for i in range(1, n + 1):
        si = (s + sum([a_s[j - 1] * pow(i, j, p) for j in range(1, t)])) % p
        s_list.append((i, si))
        print(f"Udział {i}: {si}")
    return s_list, p

def shamir_secret_reconstruction(shares, p):
    # Rekonstrukcja sekretu Shamir
    t = len(shares)
    secret = 0

    for i in range(t):
        xi, si = shares[i]
        li = 1
        for j in range(t):
            if i != j:
                xj, sj = shares[j]
                num = (-xj) % p
                den = (xi - xj) % p
                li = (li * num * modInverse(den, p)) % p

        term = (si * li) % p
        secret = (secret + term) % p
        print(f"Krok {i+1}: si={si}, L_{i}(0)={li} -> iloczyn częściowy: {term}")

    return secret % p

if __name__ == "__main__":
    # Trywialny podział sekretu
    print("Trywialny podział sekretu:")
    s_list, k = trivial_secret_sharing(5, 10)
    secret = trivial_secret_reconstruction(s_list, k)
    print(40 * '=')

    # Podział sekretu Shamir
    print("Podział sekretu Shamir:")
    udzialy, p = shamir_secret_sharing(5, 3, 500, 503)
    wybrane_udzialy = random.sample(udzialy, 3) # Zbieramy t udziałów
    odtworzony_s = shamir_secret_reconstruction(wybrane_udzialy, p)
    print(f"Oryginalny sekret: 500, Odtworzony sekret: {odtworzony_s}")
    print(40 * '=')