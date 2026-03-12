import secrets
import sympy

def generate_blum_integer(bits):
    while True:
        candidate = secrets.randbits(bits)

        candidate = candidate | (1 << (bits - 1)) | 1

        if candidate % 4 == 3:
            if sympy.isprime(candidate):
                return candidate
            
def generate_blum_integer_pair(bits):
    p = generate_blum_integer(bits)
    q = generate_blum_integer(bits)
    while p == q:
        q = generate_blum_integer(bits)
    
    N = p * q

    return p, q, N

def seed_generator(N):
    while True:
        seed = secrets.randbelow(N)
        if seed > 1 and sympy.gcd(seed, N) == 1:
            return seed
        
def blum_blum_shub(bits, output_length):
    p, q, N = generate_blum_integer_pair(bits)
    x = seed_generator(N)

    x0 = pow(x, 2, N)
    output = ""

    x_now = x0
    for _ in range(output_length):
        x_next = pow(x_now, 2, N)
        output_bit = x_next & 1
        output += str(output_bit)
        x_now = x_next
    return output

def monobit_test(output):
    count_1 = output.count('1')
    print(f"Number of 1s: {count_1}")
    if 9725 < count_1 < 10275:
        return True

def runs_test(output):
    counts_0 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    counts_1 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    current_bit = output[0]
    length = 1

    for bit in output[1:]:
        if bit == current_bit:
            length += 1
        else:
            idx = min(length, 6)
            
            if current_bit == '0':  
                counts_0[idx] += 1
            else:
                counts_1[idx] += 1

            current_bit = bit
            length = 1
    
    idx = min(length, 6)
    if current_bit == '0':
        counts_0[idx] += 1
    else:
        counts_1[idx] += 1

    ranges = {
        1: (2315, 2685),
        2: (1114, 1386),
        3: (527, 723),
        4: (240, 384),
        5: (103, 209),
        6: (103, 209)
    }

    result = {}
    for k in ranges:
        low, high = ranges[k]
        passed_0 = low <= counts_0[k] <= high
        passed_1 = low <= counts_1[k] <= high
        print(f"For 0: {low}, {high} |  {counts_0[k]}")
        print(f"For 1: {low}, {high} |  {counts_1[k]}")

        result[k] = passed_0 and passed_1

    return result

def long_run_test(output):
    zeros_long_series = '0' * 26
    ones_long_series = '1' * 26

    if zeros_long_series in output or ones_long_series in output:
        return False
    return True

def poker_test(output):
    output_pieces = [output[i:i+4] for i in range(0, len(output), 4)]
    counts = {f"{i:04b}": 0 for i in range(16)}

    for piece in output_pieces:
        counts[piece] += 1

    for piece, count in counts.items():
        print(f"{piece}: {count}")

    square_sum = sum(count**2 for count in counts.values())

    X = 16 / 5000 * square_sum - 5000 
    print(f"X: {X}")
    if 2.16 < X < 46.17:
        return True
    return False


if __name__ == "__main__":
    bits = 14
    output_length = 20_000
    random_bits = blum_blum_shub(bits, output_length)
    
    print("=== Generated Random Bits ===\n")
    print("=== Monobit Test ===")
    if monobit_test(random_bits):
        print("+++ Monobit test passed. +++\n")
    else:
        print("--- Monobit test failed. ---\n")

    print("=== Runs Test ===")
    runs_test_result = runs_test(random_bits)
    passed_all = all(runs_test_result.values())
    for k, passed in runs_test_result.items():
        if passed:
            print(f"+ Run of length {k} passed. +")
        else:
            print(f"- Run of length {k} failed. -")
    if passed_all:
        print("+++ Runs test passed. +++\n")
    else:
        print("--- Runs test failed. ---\n")
    print()

    print("=== Long Run Test ===")
    if long_run_test(random_bits):
        print("+++ Long run test passed. +++\n")
    else:
        print("--- Long run test failed. ---\n")

    print("=== Poker Test ===")
    if poker_test(random_bits):
        print("+++ Poker test passed. +++\n")
    else:
        print("--- Poker test failed. ---\n")