import hashlib
import time
import os
import random

"""Short description of each hash function in markdown file - funkcje_skrotu.md"""

# Functions
def compare_hashes(text):
    algorithms = [
        'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
        'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512'
    ]

    col_algo = 12
    col_time = 12
    col_len = 20
    row_fmt = f"{{:<{col_algo}}} | {{:>{col_time}}} | {{:>{col_len}}} | {{:>{col_len}}}"

    print(row_fmt.format("Algorytm", "Czas [ms]", "Długość (HEX)", "Podgląd skrótu"))
    print("-" * (col_algo + col_time + 2 * col_len + len("Podgląd skrótu")))

    data = text.encode()
    for algo in algorithms:
        start = time.perf_counter()
        for _ in range(100):
            h = hashlib.new(algo, data).hexdigest()
        end = time.perf_counter()

        execution_time = (end - start) * 10  # mean time in ms
        print(row_fmt.format(algo, f"{execution_time:.4f}", str(len(h)), f"{h[:20]}..."))

def find_collision():
    seen = {}
    i = 0
    while True:
        text = str(i).encode()
        h = hashlib.sha256(text).hexdigest()[:3]
        if h in seen:
            return seen[h], str(i), h
        
        seen[h] = str(i)
        i += 1

def randomness_of_hashes(algorithm, text, iterations=1000):
    original_bytes = bytearray(text.encode())
    diff_ratios = []

    for _ in range(iterations):
        h1 = hashlib.new(algorithm, original_bytes).hexdigest()
        h1_bin = bin(int(h1, 16))[2:].zfill(len(h1) * 4)

        modified_bytes = bytearray(original_bytes)
        byte_idx = random.randrange(len(modified_bytes))
        bit_idx = random.randrange(8)
        
        modified_bytes[byte_idx] ^= (1 << bit_idx)

        h2 = hashlib.new(algorithm, modified_bytes).hexdigest()
        h2_bin = bin(int(h2, 16))[2:].zfill(len(h2) * 4)

        diffs = sum(1 for b1, b2 in zip(h1_bin, h2_bin) if b1 != b2)
        diff_ratios.append(diffs / len(h1_bin))

    average_sac = (sum(diff_ratios) / len(diff_ratios)) * 100
    print(f"Średni wynik SAC po {iterations} próbach: {average_sac:.2f}%")



if __name__ == "__main__":
    compare_hashes("Hello World!")
    print("\nZnajdowanie kolizji dla SHA-256 (3 pierwsze znaki):")
    collision = find_collision()
    if collision:
        val1, val2, h_prefix = collision
        print(f"Kolizja! '{val1}' i '{val2}' mają ten sam prefix: {h_prefix}")

    print("\nLosowość hashy dla SHA-256:")
    algorithms = [
        'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
        'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512'
    ]
    for algo in algorithms:
        print(f"\nLosowość hashy dla {algo}:")
        randomness_of_hashes(algo, "Lorem ipsum dolor sit amet", iterations=1000)
