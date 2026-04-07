import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import time

# ECB, CBC,	OFB, CFB, CTR.

def stworz_plik(nazwa_pliku, rozmiar_kb):
    nazwa_pliku = f"{nazwa_pliku}"
    with open(nazwa_pliku, 'wb') as f:
        f.write(os.urandom(rozmiar_kb * 1024))

def szyfruj_plik(nazwa_pliku, klucz, tryb):
    with open(nazwa_pliku, 'rb') as f:
        dane = f.read()

    if tryb == 'ECB':
        cipher = AES.new(klucz, AES.MODE_ECB)
        zaszyfrowane = cipher.encrypt(pad(dane, AES.block_size))
        with open(f"ecb_{nazwa_pliku}", 'wb') as f:
            f.write(zaszyfrowane)
    elif tryb == 'CBC':
        cipher = AES.new(klucz, AES.MODE_CBC)
        iv = cipher.iv
        zaszyfrowane = cipher.encrypt(pad(dane, AES.block_size))
        with open(f"cbc_{nazwa_pliku}", 'wb') as f:
            f.write(iv)
            f.write(zaszyfrowane)
    elif tryb == 'OFB':
        cipher = AES.new(klucz, AES.MODE_OFB)
        iv = cipher.iv
        zaszyfrowane = cipher.encrypt(dane)
        with open(f"ofb_{nazwa_pliku}", 'wb') as f:
            f.write(iv)
            f.write(zaszyfrowane)
    elif tryb == 'CFB':
        cipher = AES.new(klucz, AES.MODE_CFB)
        iv = cipher.iv
        zaszyfrowane = cipher.encrypt(dane)
        with open(f"cfb_{nazwa_pliku}", 'wb') as f:
            f.write(iv)
            f.write(zaszyfrowane)
    elif tryb == 'CTR':
        cipher = AES.new(klucz, AES.MODE_CTR)
        nonce = cipher.nonce
        zaszyfrowane = cipher.encrypt(dane)
        with open(f"ctr_{nazwa_pliku}", 'wb') as f:
            f.write(nonce)
            f.write(zaszyfrowane)
    else:
        raise ValueError("Nieznany tryb szyfrowania")

def deszyfruj_plik(nazwa_pliku, klucz, tryb):
    if tryb == 'ECB':
        with open(nazwa_pliku, 'rb') as f:
            zaszyfrowane = f.read()
        cipher = AES.new(klucz, AES.MODE_ECB)
        odszyfrowane = unpad(cipher.decrypt(zaszyfrowane), AES.block_size)
        with open(f"ecb_decrypted_{nazwa_pliku}", 'wb') as f:
            f.write(odszyfrowane)
    elif tryb == 'CBC':
        with open(nazwa_pliku, 'rb') as f:
            iv = f.read(16)  
            zaszyfrowane = f.read()
        cipher = AES.new(klucz, AES.MODE_CBC, iv=iv)
        odszyfrowane = unpad(cipher.decrypt(zaszyfrowane), AES.block_size)
        with open(f"cbc_decrypted_{nazwa_pliku}", 'wb') as f:
            f.write(odszyfrowane)
    elif tryb == 'OFB':
        with open(nazwa_pliku, 'rb') as f:
            iv = f.read(16)  
            zaszyfrowane = f.read()
        cipher = AES.new(klucz, AES.MODE_OFB, iv=iv)
        odszyfrowane = cipher.decrypt(zaszyfrowane)
        with open(f"ofb_decrypted_{nazwa_pliku}", 'wb') as f:
            f.write(odszyfrowane)
    elif tryb == 'CFB':
        with open(nazwa_pliku, 'rb') as f:
            iv = f.read(16)  
            zaszyfrowane = f.read()
        cipher = AES.new(klucz, AES.MODE_CFB, iv=iv)
        odszyfrowane = cipher.decrypt(zaszyfrowane)
        with open(f"cfb_decrypted_{nazwa_pliku}", 'wb') as f:
            f.write(odszyfrowane)
    elif tryb == 'CTR':
        with open(nazwa_pliku, 'rb') as f:
            nonce = f.read(8)  
            zaszyfrowane = f.read()
        cipher = AES.new(klucz, AES.MODE_CTR, nonce=nonce)
        odszyfrowane = cipher.decrypt(zaszyfrowane)
        with open(f"ctr_decrypted_{nazwa_pliku}", 'wb') as f:
            f.write(odszyfrowane)
    else:
        raise ValueError("Nieznany tryb szyfrowania")


def cbc_using_ecb_encrypt(nazwa_pliku, klucz):
    with open(nazwa_pliku, 'rb') as f:
        dane = f.read()

    cipher_ecb = AES.new(klucz, AES.MODE_ECB)
    iv = get_random_bytes(AES.block_size)  
    poprzedni_blok = iv

    dane_padding = pad(dane, AES.block_size)
    
    zaszyfrowane = bytearray()
    for i in range(0, len(dane_padding), AES.block_size):
        blok = dane_padding[i: i + AES.block_size]
        aktualny_blok = bytes(a ^ b for a, b in zip(blok, poprzedni_blok))
        aktualny_blok = cipher_ecb.encrypt(aktualny_blok)
        zaszyfrowane.extend(aktualny_blok)
        poprzedni_blok = aktualny_blok

    with open(f"cbc_ecb_{nazwa_pliku}", 'wb') as f:
        f.write(iv)
        f.write(zaszyfrowane)

def cbc_using_ecb_decrypt(nazwa_pliku, klucz):
    with open(nazwa_pliku, 'rb') as f:
        iv = f.read(AES.block_size)  
        zaszyfrowane = f.read()

    cipher_ecb = AES.new(klucz, AES.MODE_ECB)
    poprzedni_blok = iv

    odszyfrowane = bytearray()
    for i in range(0, len(zaszyfrowane), AES.block_size):
        aktualny_blok = zaszyfrowane[i: i + AES.block_size]
        odszyfrowany_blok = cipher_ecb.decrypt(aktualny_blok)
        odszyfrowany_blok = bytes(a ^ b for a, b in zip(odszyfrowany_blok, poprzedni_blok))
        odszyfrowane.extend(odszyfrowany_blok)
        poprzedni_blok = aktualny_blok

    odszyfrowane = unpad(odszyfrowane, AES.block_size)
    with open(f"cbc_ecb_decrypted_{nazwa_pliku}", 'wb') as f:
        f.write(odszyfrowane)

if __name__ == "__main__":
    random_bytes = get_random_bytes(64)
    key = get_random_bytes(32)  
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(random_bytes, AES.block_size))
    

    nazwy_plikow = ["plik10KB.bin", "plik10MB.bin", "plik100MB.bin"]
    rozmiary = [10, 10 * 1024, 100 * 1024]  # w KB

    for nazwa, rozmiar in zip(nazwy_plikow, rozmiary):
        stworz_plik(nazwa, rozmiar)

    rozszerzenia = ['ecb_', 'cbc_', 'ofb_', 'cfb_', 'ctr_']
    tryby = ['ECB', 'CBC', 'OFB', 'CFB', 'CTR']

    nowe_pliki = [f"{tryb}{nazwa}" for nazwa in nazwy_plikow for tryb in rozszerzenia]
    klucz = get_random_bytes(32)  # 256-bitowy klucz

    czasy_szyfrowania = {}
    czasy_deszyfrowania = {}

    for plik in nazwy_plikow:
        for tryb in tryby:
            start = time.perf_counter()
            szyfruj_plik(plik, klucz, tryb)
            end = time.perf_counter()
            czasy_szyfrowania[f"{plik}_{tryb}"] = (end - start) * 1000  # czas w ms

    for plik in nowe_pliki:
        for rozszerzenie, tryb in zip(rozszerzenia, tryby):
            if plik.startswith(rozszerzenie):
                tryb_szyfrowania = tryb
                start = time.perf_counter()
                deszyfruj_plik(plik, klucz, tryb_szyfrowania)
                end = time.perf_counter()
                czasy_deszyfrowania[f"{plik}"] = (end - start) * 1000  # czas w ms

    print("Czasy szyfrowania (ms):")
    for key, value in czasy_szyfrowania.items():
        print(f"{key}: {value:.2f} ms")

    print("\nCzasy deszyfrowania (ms):")
    for key, value in czasy_deszyfrowania.items():
        print(f"{key}: {value:.2f} ms")
    