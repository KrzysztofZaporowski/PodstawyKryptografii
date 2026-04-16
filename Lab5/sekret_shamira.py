import random

def trivial_secret_sharing(n, k):
    s = random.choice(range(0, k))
    s_list = []
    for _ in range(n - 1):
        print(_)
        s_list.append(random.choice(range(0, k)))
    s_n = (s - sum(s_list)) % k
    s_list.append(s_n)
    print(f"Udziały: {s_list}")
   
if __name__ == "__main__":
    trivial_secret_sharing(5, 10)