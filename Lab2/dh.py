import secrets
import sympy

def define_public_values():
    n = sympy.randprime(1000, 10000)
    g = sympy.ntheory.primitive_root(n)

    if 1 < g < n:
        return n, g

def A_steps(values):
    n, g = values
    x = secrets.randbelow(10000)
    X = pow(g, x, n)

    return x, X

def B_steps(values):
    n, g = values
    y = secrets.randbelow(10000)
    Y = pow(g, y, n)

    return y, Y

def compute_shared_secret_A(x, Y, values):
    n, g = values
    k = pow(Y, x, n)
    return k

def compute_shared_secret_B(y, X, values):
    n, g = values
    k = pow(X, y, n)
    return k

if __name__ == "__main__":
    # Define public values
    public_values = define_public_values()
    print(f"Public values (n, g): {public_values}")
    print("=" * 40)

    # A's steps
    x, X = A_steps(public_values)
    print(f"A's private value (x): {x}")
    print(f"A's public value (X): {X}")
    print("=" * 40)

    # B's steps
    y, Y = B_steps(public_values)
    print(f"B's private value (y): {y}")
    print(f"B's public value (Y): {Y}")
    print("=" * 40)

    # Compute shared secrets
    shared_secret_A = compute_shared_secret_A(x, Y, public_values)
    shared_secret_B = compute_shared_secret_B(y, X, public_values)
    print(f"A's computed shared secret: {shared_secret_A}")
    print(f"B's computed shared secret: {shared_secret_B}")